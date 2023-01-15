import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DATABASE_ROOT_USER")
password = os.getenv("DATABASE_ROOT_PASSWORD")

async def get_db():
    client = AsyncIOMotorClient(f"mongodb+srv://{user}:{password}@darkcodecamp.rmiy3fz.mongodb.net/test")
    db = client.blog_db
    blogpost_collection = db.blogpost
    users_collection = db.users
    return blogpost_collection, users_collection
