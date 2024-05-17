from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from resolver import random_movies, random_genres_movies, user_login
from recommender import movie_based_recommendation, user_based_recommendation, user_rating_based_recommendation
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
    return JSONResponse(status_code=200, content={"success": True, "data": result})

@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    result = random_genres_movies(genre)
    return JSONResponse(status_code=200, content={"success": True, "data": result})

@app.get("/movie-based/{movie_id}")
async def item_based(movie_id):
    result = movie_based_recommendation(movie_id)
    return JSONResponse(status_code=200, content={"success": True, "data": result})

@app.get("/user-based/{user_id}")
async def user_based(user_id):
    result = user_based_recommendation(user_id)
    return JSONResponse(status_code=200, content={"success": True, "data": result})

@app.get("/user-rating-based")
async def user_rating_based(params: Optional[List[str]] = Query(None)):
    input_rating_dict = dict((int(x.split(":")[0]), float(x.split(":")[1])) for x in params)
    result = user_rating_based_recommendation(input_rating_dict)
    return JSONResponse(status_code=200, content={"success": True, "data": result})

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
async def login(loginParams: UserLogin):
    result = user_login(loginParams.email, loginParams.password)
    if not result:
        err_msg = "No user found with given email and password"
        return JSONResponse(status_code=404, content={"success": False, "error": err_msg, "data": None})
    else:
        return JSONResponse(status_code=200, content={"success": True, "message": "successfully logged in", "data": result})
