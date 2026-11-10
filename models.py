from datetime import datetime, timezone
from decimal import Decimal 
from sqlalchemy import create_engine, Numeric, ForeignKey 
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal('0.00'))


class TransactionDB(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'))  
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

