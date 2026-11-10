import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from decimal import Decimal 
from schemas import TransferIn

from database import get_db
from models import UserDB, TransactionDB
from security import ALGHORITHM, SECRET_KEY

router = APIRouter(prefix="/wallet", tags=["Wallet"])

security_scheme = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGHORITHM])
        user_id_str: str | None = payload.get("sub")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return int(user_id_str)

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/balance")
def balance(user_id: int = Depends(get_current_user_id),  db: Session = Depends(get_db)):
    user = db.scalar(select(UserDB).where(UserDB.id == user_id))

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": user.username, "balance": user.balance}


@router.post("/transfer")  
def transfer(transfer_in: TransferIn,  db: Session = Depends(get_db),user_id: int = Depends(get_current_user_id)):
    sender = db.scalar(
        select(UserDB).where(UserDB.id == user_id).with_for_update()
    )
    receiver = db.scalar(
        select(UserDB).where(UserDB.username == transfer_in.receiver_username).with_for_update()
    )

    if sender is None or receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Sender or Receiver not found"
        )

    if sender.id == receiver.id:
        raise HTTPException(status_code=400, detail="You cannot transfer money to yourself")

    if sender.balance < transfer_in.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender.balance -= transfer_in.amount
    receiver.balance += transfer_in.amount

    new_transaction = TransactionDB(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=transfer_in.amount
    )
    db.add(new_transaction)

    db.commit()

    return {
        "status": "success",
        "message": f"Successfully transferred {transfer_in.amount} to {receiver.username}",
        "new_balance": sender.balance
    }

