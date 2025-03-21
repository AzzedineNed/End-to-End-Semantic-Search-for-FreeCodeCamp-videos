import requests
import json
import polars as pl
from sentence_transformers import SentenceTransformer
import os

def getVideoRecords(response: requests.models.Response) -> list:
    """Extracts video metadata from YouTube API response."""
    video_record_list = []
    data = json.loads(response.text)

    for item in data.get('items', []):
        video_record = {
            'video_id': item['contentDetails']['videoId'],
            'datetime': item['contentDetails']['videoPublishedAt'],
            'title': item['snippet']['title']
        }
        video_record_list.append(video_record)

    return video_record_list

def getVideoIDs():
    """Fetches video IDs and titles from FreeCodeCamp's YouTube channel."""
    api_key = os.getenv('YT_API_KEY')
    channel_id = 'UC8butISFwT-Wl7EV0hUK0BQ'  # FreeCodeCamp channel: UC8butISFwT-Wl7EV0hUK0BQ , shaws's: UCa9gErQ9AE5jT2DZLjXBIdA
    base_url = 'https://www.googleapis.com/youtube/v3/playlistItems'

    # Get Uploads Playlist ID
    playlist_response = requests.get(
        f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={api_key}"
    )
    if playlist_response.status_code != 200:
        print(f"Channel API Error: {playlist_response.text}")
        return

    playlist_id = json.loads(playlist_response.text)['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    print(f"Uploads Playlist ID: {playlist_id}")

    page_token = None
    video_record_list = []

    while True:
        params = {
            "key": api_key,
            "playlistId": playlist_id,
            "part": "contentDetails,snippet",
            "maxResults": 50,
            "pageToken": page_token
        }

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Playlist Items API Error: {response.text}")
            break

        new_videos = getVideoRecords(response)
        video_record_list.extend(new_videos)
        print(f"Fetched {len(video_record_list)} videos...")

        data = json.loads(response.text)
        page_token = data.get('nextPageToken', None)
        if not page_token:
            break

    df = pl.DataFrame(video_record_list)
    df.write_parquet('app/data/video-ids.parquet')
    print(f"✅ Saved {len(video_record_list)} video IDs to video-ids.parquet")

def getVideoDescriptions():
    """Fetches descriptions for all videos using YouTube API."""
    api_key = os.getenv('YT_API_KEY')
    df = pl.read_parquet('app/data/video-ids.parquet')
    descriptions = []

    for video_id in df['video_id']:
        try:
            response = requests.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    'key': api_key,
                    'id': video_id,
                    'part': 'snippet'
                }
            )
            if response.status_code == 200:
                description = json.loads(response.text)['items'][0]['snippet']['description']
            else:
                description = "n/a"
        except Exception as e:
            print(f"Error fetching description for {video_id}: {str(e)}")
            description = "n/a"
        
        descriptions.append(description)

    df = df.with_columns(pl.Series(name="description", values=descriptions))
    df.write_parquet('app/data/video-descriptions.parquet')
    print("✅ Added descriptions to dataset")

def setDatatypes(df: pl.DataFrame) -> pl.DataFrame:
    """Sets proper data types for DataFrame columns."""
    df = df.with_columns(pl.col('datetime').cast(pl.Datetime))
    return df

def transformData():
    """Preprocesses and cleans the video data."""
    df = pl.read_parquet('app/data/video-descriptions.parquet')
    df = setDatatypes(df)
    df.write_parquet('app/data/video-descriptions.parquet')

def createTextEmbeddings():
    """Generates embeddings for video titles and descriptions."""
    df = pl.read_parquet('app/data/video-descriptions.parquet')
    
    # Filter out videos without descriptions
    df = df.filter(pl.col("description") != "n/a")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    column_name_list = ['title', 'description']

    for column_name in column_name_list:
        embedding_arr = model.encode(df[column_name].to_list())
        
        # Create embedding columns
        schema_dict = {f"{column_name}_embedding_{i}": pl.Float64 for i in range(embedding_arr.shape[1])}
        df_embeddings = pl.DataFrame(embedding_arr, schema=schema_dict)
        
        df = df.hstack(df_embeddings)

    df.write_parquet('app/data/video-index.parquet')
    print(f"✅ Created embeddings for {len(df)} videos")
