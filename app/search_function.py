import numpy as np
import polars
import sentence_transformers
import sklearn
from sklearn.metrics import DistanceMetric

# helper function
def returnSearchResultIndexes(query: str, 
                              df: polars.DataFrame,  # Change LazyFrame to DataFrame here
                              model, 
                              dist: DistanceMetric) -> np.ndarray:
    """
        Function to return indexes of top search results
    """
    
    # embed query
    query_embedding = model.encode(query).reshape(1, -1)
    
    # compute distances between query and titles/transcripts
    # Convert df to numpy array for distance computation, no need for collect() if it's a DataFrame
    dist_arr = dist.pairwise(df[:, 4:388].to_numpy(), query_embedding) + dist.pairwise(df[:, 388:].to_numpy(), query_embedding)

    # search parameters
    threshold = 40  # eye-balled threshold for manhattan distance
    top_k = 20

    # evaluate videos close to query based on threshold
    idx_below_threshold = np.argwhere(dist_arr.flatten() < threshold).flatten()
    # keep top k closest videos
    idx_sorted = np.argsort(dist_arr[idx_below_threshold], axis=0).flatten()

    # return indexes of search results
    return idx_below_threshold[idx_sorted][:top_k]
