import uvicorn
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.wallet import router as wallet_router

app = FastAPI(title="FinTech P2P Wallet API")

app.include_router(auth_router)
app.include_router(wallet_router)


@app.get("/")
def read_root():
    return {"status": "working", "project": "P2P Wallet"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
