from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from datetime import datetime
from bson import ObjectId, json_util
from utils.mongo_dao import get_db
import json

from models.blogModel import BlogPost, RespModel, AllBlogpostResponse
from models.userModel import User
from models.authModel import UserJWT

app = FastAPI()

@app.get("/blogpost", response_model=AllBlogpostResponse)
async def get_all_blogpost():
    try:
        # Connect to the database
        blogpost_collection, _ = await get_db()

        # Get all blog posts from the database
        blogposts = await blogpost_collection.find().to_list(length=100)

        # Return the blog posts
        return AllBlogpostResponse(response=blogposts)
    except Exception as e:
        # Handle any exceptions that may occur
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")


@app.get("/blogpost/{id}", response_model=RespModel)
async def get_blogpost(id: str):
    try:
        # Connect to the database
        blogpost_collection, _ = await get_db()

        # Validate the id parameter
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid blog post ID")

        # Get the blog post from the database
        blogpost = await blogpost_collection.find_one({"_id": ObjectId(id)})

        # Check if the blog post exists
        if blogpost:
            # Return the blog post
            return blogpost
        else:
            # Raise an exception if the blog post does not exist
            raise HTTPException(status_code=404, detail="Blog post not found")
    except Exception as e:
        # Handle any exceptions that may occur
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")
        

@app.post("/blogpost", response_model=RespModel)    
async def create_blogpost(blogpost: BlogPost):
    try:
        # Connect to the database
        blogpost_collection, _ = await get_db()

        # Insert the blog post into the database
        result = await blogpost_collection.insert_one(blogpost.dict())

        # Check if the insertion was successful
        if result.acknowledged:
            # Return the inserted blog post
            return blogpost.dict()
        else:
            # Raise an exception if the insertion was not successful
            raise HTTPException(status_code=400, detail="Error creating blog post")
    except pymongo.errors.DuplicateKeyError as e:
        raise HTTPException(status_code=400, detail="Duplicate key error")
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=503, detail="Unable to connect to the database")
    except Exception as e:
        # Handle any other exceptions that may occur
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")


@app.delete("/blogpost/{id}")
async def delete_blogpost(id: str):
    try:
        # Connect to the database
        blogpost_collection, _ = await get_db()

        # Validate the id parameter
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid blog post ID")

        # Delete the blog post from the database
        result = await blogpost_collection.delete_one({"_id": ObjectId(id)})

        # Check if the deletion was successful
        if result.deleted_count == 0:
            # Raise an exception if the deletion was not successful
            raise HTTPException(status_code=404, detail="Blog post not found")
        else:
            # Return the deleted blog post ID
            return {"id": id}
    except Exception as e:
        # Handle any exceptions that may occur
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")



@app.put("/blogpost/{id}", response_model=RespModel)
async def update_blogpost(id: str, blogpost: BlogPost):
    try:
        # Connect to the database
        blogpost_collection, _ = await get_db()

        # Validate the id parameter
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid blog post ID")

        # Check if the blog post exists
        existing_blogpost = await blogpost_collection.find_one({"_id": ObjectId(id)})
        if not existing_blogpost:
            raise HTTPException(status_code=404, detail="Blog post not found")

        # Update the blog post in the database
        result = await blogpost_collection.replace_one({"_id": ObjectId(id)}, blogpost.dict())

        # Check if the update was successful
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Error updating blog post")
        else:
            # Return the updated blog post
            return blogpost.dict()
    except Exception as e:
        # Handle any exceptions that may occur
        print(str(e))
        raise HTTPException(status_code=500, detail="Server Error")
