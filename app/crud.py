from sqlalchemy.orm import Session
from app.models import User as DBUser, Review as DBReview
from app.schemas import UserCreate, ReviewCreate, User as SchemaUser
from app.auth import get_passwordHash

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(DBUser).offset(skip).limit(limit).all()

def createUser(db: Session, user: UserCreate):
    hashed_password = get_passwordHash(user.password)
    db_user = DBUser(username=user.username, hashed_password=hashed_password)  # bruk DBUser her!
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_review(db: Session, review: ReviewCreate, user_id: int):
    db_review = DBReview(**review.dict(), owner_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review

def get_reviews(db: Session, skip: int= 0, limit: int =10):
    return db.query(DBReview).offset(skip).limit(limit).all()

def delete_review(db: Session, review: DBReview, user: DBUser):
    review = db.query(DBReview).filter(DBReview.id == review.id).first()
    if not review:
        raise Exception("No review found")

    if review.owner_id != user.id:
        raise Exception("Not the owner of the review")

    db.delete(review)
    db.commit()

def update_review(review_id: int, review_update: ReviewCreate, db: Session, current_user: DBUser):

    review_in_db = db.query(DBReview).filter(DBReview.id == review_id).first()
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


    return DBReview.from_orm(review_in_db)

