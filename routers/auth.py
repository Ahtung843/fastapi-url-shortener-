from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import UserDB
from schemas import UserAuth
from security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(user_in: UserAuth, db: Session = Depends(get_db)):
    user = db.scalar(select(UserDB).where(UserDB.username == user_in.username))

    if user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user_in.password)

    db_user = UserDB(
        username=user_in.username,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "id": db_user.id,
        "username": db_user.username,
        "balance": db_user.balance,
    }


@router.post("/login")
def loging(user_in: UserAuth, db: Session = Depends(get_db)):
    check_user = db.scalar(
        select(UserDB).where(UserDB.username == user_in.username)
    )
    is_password_correct = False
    if check_user:
        is_password_correct = verify_password(
            user_in.password, check_user.hashed_password
        )
    else:
        verify_password(user_in.password, "dummy_hash_for_timing_attack")

    if not check_user or not is_password_correct:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    token = create_access_token(user_id=check_user.id)

    return {"access_token": token, "token_type": "bearer"}
