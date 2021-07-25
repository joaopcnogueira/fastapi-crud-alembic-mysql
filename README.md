# Install Python 3.9.6

Go to https://www.python.org/downloads/release/python-396/

# Setup up the Environment
```
python -m venv venv
./venv/Scripts/activate.bat
pip install fastapi uvicorn sqlalchemy alembic fastapi_sqlalchemy pymysql python-dotenv
```

# Initiate the Alembic Folder
```bash
alembic init alembic
```
# Bind the Database to Alembic

He we are using a mysql database. First, create a mysql database called `fastapi_db` with Charset `utf8mb4` and Collation `utf8mb4_general_ci`. 

Set the variable `SQLALCHEMY_DATABASE_URI` from the `.env` file as:

```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root@localhost/fastapi_db
```

Note: we should have mysql up and running in your machine with a root user with a blank password.

# Create the Models

Create a file `sql_app/models.py` inside your project folder and put the following content inside it:

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

# Connect Alembic Migrations with Models

This is to let alembic knows which models to use to create the migrations.

At the `alembic/env.py` file, right after the line 19, add the following lines of code:

```python
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "sql_app"))

import models
target_metadata = models.Base.metadata
```

and delete the line `target_metadata = None`


# Do the First Migration

```
alembic revision --autogenerate -m "first revision"
alembic upgrade head
```

Now, if you open the database, you should see the created database with the empty tables `users` and `items`.


# CRUD Operations

All the CRUD operations are in the file `sql_app/crud.py`


# Main FastAPI app

The fastapi app are in the file `sql_app/main.py`

# Do the CRUD!

Start up the server by executing:
```
uvicorn sql_app.main:app --reload
```

and go to
```
http://127.0.0.1:8000/docs
```

# References
1. [Creating a CRUD App with FastAPI](https://gabbyprecious.medium.com/creating-a-crud-app-with-fastapi-part-one-7c049292ad37)
2. https://fastapi.tiangolo.com/tutorial/sql-databases/