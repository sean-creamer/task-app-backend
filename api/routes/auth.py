import json
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import security
from database.db import get_db
from models.users import User
from schemas.auth import Token
from schemas.users import UserCreate
from security import verify_password, hash_password

router = APIRouter()


@router.post("/signup")
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db),
):
    # Hash the user's password
    hashed_password = hash_password(user.password)

    # Create a new user instance
    db_user = User(username=user.username, hashed_password=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully", "user": {"username": db_user.username, "id": db_user.id}}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username already exists")
    finally:
        db.close()


@router.post("/login", response_model=Token)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(form_data.password, str(user.hashed_password)):
        raise HTTPException(status_code=400, detail="Incorrect password")

    expire = timedelta(minutes=30)
    access_token = security.create_access_token(
        subject=json.dumps({"username": user.username, "id": user.id}),
        expires_delta=expire
    )

    return {"access_token": access_token, "token_type": "bearer"}
