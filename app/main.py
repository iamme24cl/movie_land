from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resolver import random_movies, random_genres_movies, user_login
from recommender import movie_based_recommendation, user_based_recommendation
from pydantic import BaseModel

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.get("/movie-based/{movie_id}")
async def item_based(movie_id):
    result = movie_based_recommendation(movie_id)
    return {"result": result}

@app.get("/user-based/{user_id}")
async def user_based(user_id):
    result = user_based_recommendation(user_id)
    return {"result": result}

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(loginParams: UserLogin):
    result = user_login(loginParams.email, loginParams.password)
    return {"result": result}
