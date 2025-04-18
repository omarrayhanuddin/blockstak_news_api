from fastapi import FastAPI, Depends
from src.database.database import engine
from src.models.news import Base
from src.auth.oauth2 import oauth2_scheme, verify_token
from src.routers import news, auth

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Blockstak News API")

app.include_router(auth.router)
app.include_router(
    news.router,
    prefix="/news",
    tags=["news"],
    dependencies=[Depends(oauth2_scheme), Depends(verify_token)],
)
