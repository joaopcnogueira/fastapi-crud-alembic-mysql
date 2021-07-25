from typing import List
from fastapi import FastAPI, HTTPException

from . import crud, schemas
from fastapi_sqlalchemy import DBSessionMiddleware

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url='mysql+pymysql://root@localhost/fastapi_db')


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(skip=skip, limit=limit)
    return items
