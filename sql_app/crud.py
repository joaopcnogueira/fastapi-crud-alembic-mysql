from . import models, schemas
from fastapi_sqlalchemy import db


def get_user(user_id: int):
    return db.session.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return db.session.query(models.User).filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return db.session.query(models.User).offset(skip).limit(limit).all()


def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user


def get_items(skip: int = 0, limit: int = 100):
    return db.session.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.session.add(db_item)
    db.session.commit()
    db.session.refresh(db_item)
    return db_item