from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import security
from database.db import get_db
from models.users import User

router = APIRouter()


@router.get("/users")
def get_users(
        db: Session = Depends(get_db),
        _: str = Depends(security.token_required),
):
    try:
        users = db.query(User).all()
        return [{"id": user.id, "username": user.username} for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")
