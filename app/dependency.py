from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import session
from app.models import User
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db) ):
    wrong_credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot validate credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise wrong_credentials
    except JWTError:
        raise wrong_credentials

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise wrong_credentials
    return user
