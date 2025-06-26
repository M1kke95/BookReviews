from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    bio = Column(String)
    hashed_password = Column(String)
    reviewsByUser = relationship("Review", back_populates="owner")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(Integer, index=True, unique=True)
    title = Column(String, index=True)
    summary = Column(String)
    reviews = relationship("Review", back_populates='book')


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String)
    review_text = Column(String)
    rating = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    owner = relationship("User", back_populates="reviewsByUser")
    book = relationship("Book", back_populates="reviews")