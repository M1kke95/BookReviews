from sqlalchemy.orm import Session
from models import User, Review
from schemas import UserCreate, ReviewCreate, User
from auth import get_passwordHash

def createUser(db: Session, user: UserCreate):
    hashed_password = get_passwordHash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def create_review(db: Session, review: ReviewCreate, user_id: int):
    db_review = Review(**review.dict(), owner_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

def get_reviews(db: Session, skip: int= 0, limit: int =10):
    return db.query(Review).offset(skip).limit(limit).all()

def delete_review(db: Session, review: Review, user: User):
    review = db.query(Review).filter(Review.id == review.id).first()
    if not review:
        raise Exception("No review found")

    if review.owner_id != user.id:
        raise Exception("Not the owner of the review")

    db.delete(review)
    db.commit()

def update_review(review_id: int, review_update: ReviewCreate, db: Session, current_user: User):

    review_in_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_in_db:
        raise Exception("Review not found")
    if review_in_db.owner_id != current_user.id:
        raise Exception("Not authorized")

    changed = False

    if review_in_db.book_title != review_update.book_title:
        review_in_db.book_title = review_update.book_title
        changed = True
    if review_in_db.review_text != review_update.review_text:
        review_in_db.review_text = review_update.review_text
        changed = True
    if review_in_db.rating != review_update.rating:
        review_in_db.rating = review_update.rating
        changed = True

    if changed:
       db.commit()
       db.refresh(review_in_db)


    return Review.from_orm(review_in_db)

