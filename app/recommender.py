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
        factors=50, regularization=0.01, dtype=np.float64, iterations=50
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
    
    result = [int(x) for x in result if x != str(movie_id)]
    result_items = movies_df[movies_df["movieId"].isin(result)].to_dict("records")
    return result_items

def calculate_user_based(user_items, items, userId):
    loaded_model = pickle.load(open(saved_model,"rb"))
    recs = loaded_model.recommend(userid=userId, user_items=user_items, recalculate_user=True, N=10)
    return [str(items[r]) for r in recs[0] if r in items]

def build_matrix_input(rating_dict, items):
    model = pickle.load(open(saved_model,"rb"))
    item_ids = {r: i for i, r in enumerate(items.values())}
    mapped_idx = [item_ids[s] for s in rating_dict.keys() if s in item_ids]
    data = [weight*float(x) for x in rating_dict.values()]
    
    rows = [0 for _ in mapped_idx]
    shape = (1, model.item_factors.shape[0])
    coo_mat = coo_matrix((data, (rows, mapped_idx)), shape=shape)
    return coo_mat.tocsr() 

def user_based_recommendation(userId):
    ratings_df = pd.read_csv(ratings)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(movies)
    items = dict(enumerate(ratings_df["movieId"].cat.categories))  
    user_ratings = ratings_df[ratings_df["userId"] == int(userId)][["movieId", "rating"]]
    rating_list = []
    for ind in user_ratings.index:
        rating = str(user_ratings["movieId"][ind]) + ":" + str(user_ratings["rating"][ind])
        rating_list.append(rating)
    rating_dict = dict((int(x.split(":")[0]), float(x.split(":")[1])) for x in rating_list)
    input_matrix = build_matrix_input(rating_dict, items)
    result = calculate_user_based(input_matrix, items, userId)
    result = [int(x) for x in result]
    result_items = movies_df[movies_df["movieId"]. isin(result)].to_dict("records")    
    return result_items 

def user_rating_based_recommendation(input_rating):
    print(f"input_rating dict => {input_rating}")
    ratings_df = pd.read_csv(ratings)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(movies)
    items = dict(enumerate(ratings_df["movieId"].cat.categories))  
    input_matrix = build_matrix_input(input_rating, items)
    result = calculate_user_based(input_matrix, items, 0)
    result = [int(x) for x in result]
    result_items = movies_df[movies_df["movieId"]. isin(result)].to_dict("records")    
    return result_items 
    
if __name__ == "__main__":
    model = model_train()