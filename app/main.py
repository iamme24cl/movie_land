from fastapi import FastAPI
from resolver import random_movies, random_genres_movies

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/all")
async def all_movies():
    result = random_movies()
    return {"result": result}

@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    result = random_genres_movies(genre)
    return {"result": result}
