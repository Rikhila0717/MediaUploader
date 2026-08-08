from fastapi import FastAPI, HTTPException
from app.schemas import PostResponse, PostRequest
from app.db import Post, get_async_session, create_db_and_tables
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

text_post = {
    1: {
        "title": "Getting Started with FastAPI",
        "content": "FastAPI makes building Python APIs simple and fast."
    },
    2: {
        "title": "Learning Python",
        "content": "Python is a great language for backend development."
    },
    3: {
        "title": "Understanding REST APIs",
        "content": "REST APIs allow applications to communicate over HTTP."
    },
    4: {
        "title": "HTTP Methods",
        "content": "GET, POST, PUT, PATCH, and DELETE are common HTTP methods."
    },
    5: {
        "title": "Database Basics",
        "content": "Databases help applications store and retrieve persistent data."
    },
    6: {
        "title": "Async Programming",
        "content": "Async programming helps applications efficiently handle I/O operations."
    },
    7: {
        "title": "API Authentication",
        "content": "Authentication verifies the identity of users accessing an API."
    },
    8: {
        "title": "Docker for Developers",
        "content": "Docker packages applications and their dependencies into containers."
    },
    9: {
        "title": "Deploying an API",
        "content": "A FastAPI application can be deployed using platforms such as AWS or Render."
    },
    10: {
        "title": "Backend Development",
        "content": "Backend development involves APIs, databases, authentication, and business logic."
    }
}

@app.get("/post")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_post.values())[:limit]
    return text_post


@app.get("/post/{id}")
def get_post_by_id(id: int):
    if id not in text_post:
        raise HTTPException(status_code=404, detail="post not found")
    return text_post.get(id)


@app.post("/post")
def create_post(post: PostRequest) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_post[max(text_post.keys())+1] = new_post
    return new_post
