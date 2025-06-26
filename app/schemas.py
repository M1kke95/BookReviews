from pydantic import BaseModel

class ReviewCreate(BaseModel):
    book_title: str
    review_text: str
    rating: int

class Review(ReviewCreate):
    id: int
    owner_id: int


class UserCreate(BaseModel):
    username: str
    password: str

class User(UserCreate):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str



