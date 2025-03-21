from fastapi import FastAPI
import polars as pl
from sentence_transformers import SentenceTransformer
from sklearn.metrics import DistanceMetric
import numpy as np
from app.search_function import returnSearchResultIndexes

# define model info
model_name = 'all-MiniLM-L6-v2'

# load model
model = SentenceTransformer(model_name)

# load video index
df = pl.read_parquet('app/data/video-index.parquet')

# create distance metric object
dist_name = 'manhattan'
dist = DistanceMetric.get_metric(dist_name)


# create FastAPI object
app = FastAPI()

# API operations
@app.get("/")
def health_check():
    return {'health_check': 'OK nh'}

@app.get("/info")
def info():
    return {'name': 'yt-search', 'description': "Search API for FreeCodeCamp's YouTube videos."}

@app.get("/search")
def search(query: str):
    idx_result = returnSearchResultIndexes(query, df, model, dist)

    # Convert idx_result to a list and use it for indexing
    idx_result_list = idx_result.tolist()  # Convert NumPy array to a Python list

    # Select the relevant rows using idx_result_list
    result_df = df.select(['title', 'video_id'])[idx_result_list]


    # Return the results as a dictionary
    return result_df.to_dict(as_series=False)

