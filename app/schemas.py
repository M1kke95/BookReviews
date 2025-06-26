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

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str



