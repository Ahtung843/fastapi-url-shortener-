from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import uvicorn
from database import SessionLocal, LinkDB
from sqlalchemy.orm import Session
import secrets

app = FastAPI(title="Мое API с PostgreSQL")

class LinkCreate(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten")
def short(link: LinkCreate, db: Session = Depends(get_db)):
    short_code = secrets.token_urlsafe(4)
    new_link = LinkDB(
        original_url=str(link.url),
        short_code=short_code
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)

    return {"short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def short_codes(short_code: str, db: Session = Depends(get_db)):
    db_link = db.query(LinkDB).filter(LinkDB.short_code == short_code).first()

    if not db_link:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    db_link.clicks += 1
    db.commit()

    return RedirectResponse(url=db_link.original_url)

@app.get("/stats/{short_code}")
def stats(short_code: str, db: Session = Depends(get_db)):
    db_link = db.query(LinkDB).filter(LinkDB.short_code == short_code).first()

    if not db_link:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")

    return {"url": db_link.original_url, "clicks": db_link.clicks}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
