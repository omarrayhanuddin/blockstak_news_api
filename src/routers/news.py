from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.services.news_service import NewsService
from src.schemas.news import NewsResponse
from src.database.database import get_db
from typing import List, Optional

router = APIRouter()
news_service = NewsService()


@router.get("/", response_model=List[dict])
async def get_news(page: int = 1, page_size: int = 10):
    return await news_service.fetch_news(page, page_size)


@router.post("/save-latest", response_model=List[NewsResponse])
async def save_latest_news(country_code: str = "us", db: Session = Depends(get_db)):
    return await news_service.fetch_and_save_latest(db, country_code)


@router.get("/headlines/country/{country_code}", response_model=List[dict])
async def get_headlines_by_country(country_code: str):
    return await news_service.fetch_headlines_by_country(country_code)


@router.get("/headlines/source/{source_id}", response_model=List[dict])
async def get_headlines_by_source(source_id: str):
    return await news_service.fetch_headlines_by_source(source_id)


@router.get("/headlines/filter", response_model=List[dict])
async def get_headlines_filtered(
    country: Optional[str] = Query(None), source: Optional[str] = Query(None)
):
    return await news_service.fetch_headlines_filtered(country, source)
