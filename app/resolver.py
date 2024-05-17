import pandas as pd

item_fname = "data/movies_final.csv"
users_fname = "data/users.csv"

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

def user_login(email, password):
    user_df = pd.read_csv(users_fname)
    
    user_exists = user_df[(user_df['email'] == email) & (user_df['password'] == password)]
    if not user_exists.empty:
        users = user_exists.to_dict("records")
        return users[0]
    else:
        return {}