from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class LinkDB(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column()
    short_code: Mapped[str] = mapped_column(unique=True, index=True)
    clicks: Mapped[int] = mapped_column(default=0)

Base.metadata.create_all(bind=engine)
