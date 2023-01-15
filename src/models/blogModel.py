from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, validator

class BlogPost(BaseModel):
    title: str
    content: str
    author: str
    date_created: datetime
    date_modified: datetime
    tags: List[str]
    featured_image: str = None
    summary: str = None
    comments: List[str] = None

    @validator("title")
    def title_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be blank.")
        return value
        
    @validator("content")
    def content_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Content cannot be blank.")
        return value
        
    @validator("author")
    def author_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Author cannot be blank.")
        return value

class RespModel(BaseModel):
    title: str
    content: str
    author: str
    date_created: datetime
    date_modified: datetime
    tags: List[str]
    featured_image: str = None
    summary: str = None
    comments: List[str] = None

class AllBlogpostResponse(BaseModel):
    response: List[BlogPost]
