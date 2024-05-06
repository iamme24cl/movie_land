import pandas as pd

item_fname = "data/movies_final.csv"

def random_movies():
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna('') # To fill the blank
    result_items = movies_df.sample(n=30).to_dict("records")
    return result_items

def random_genres_movies(genre):
    movies_df = pd.read_csv(item_fname)
    genre_df = movies_df[movies_df["genres"].apply(lambda x: genre in x.lower())]
    genre_df = genre_df.fillna('')
    result_items = genre_df.sample(n=30).to_dict("records")
    return result_items