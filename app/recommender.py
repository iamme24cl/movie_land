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

if __name__ == "__main__":
    model = model_train()