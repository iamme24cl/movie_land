import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from implicit.als import AlternatingLeastSquares
import pickle 

saved_model = "model/finalized_model.sav"
ratings = "data/ratings.csv"
movies = "data/movies_final.csv"
weight = 10

def model_train():
    ratings_df = pd.read_csv(ratings)
    # create a sparse matrix of all the users/repos
    rating_matrix = csr_matrix((
        ratings_df["rating"].astype(np.float32),
        (ratings_df["userId"], ratings_df["movieId"])
    ))
    als_model = AlternatingLeastSquares(
        factors=50, regularization=0.01, dtype=np.float64, iterations=1
    )
    als_model.fit(weight*rating_matrix)
    pickle.dump(als_model, open(saved_model,"wb"))
    return als_model

def calculate_movie_based(movie_id, movie_items):
    model = pickle.load(open(saved_model, "rb"))
    recs = model.similar_items(itemid=int(movie_id), N=11)
    return [str(movie_items[r]) for r in recs[0]]

def movie_based_recommendation(movie_id):
    ratings_df = pd.read_csv(ratings)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(movies)
    movie_items = dict(enumerate(ratings_df["movieId"].cat.categories))
    try:
        parsed_id = ratings_df["movieId"].cat.categories.get_loc(int(movie_id))
        result = calculate_movie_based(parsed_id, movie_items)
    except KeyError as e:
        result = []
    
    result = [int(x) for x in result if x != movie_id]
    result.pop(0) # remove the movie with item_id
    result_items = movies_df[movies_df["movieId"].isin(result)].to_dict("records")
    return result_items

if __name__ == "__main__":
    model = model_train()