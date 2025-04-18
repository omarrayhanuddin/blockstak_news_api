import httpx
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.models.news import News
from src.schemas.news import NewsCreate
from src.config import settings
from typing import List, Optional
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class NewsService:
    def __init__(self):
        self.base_url = "https://newsapi.org/v2"
        self.api_key = settings.NEWS_API_KEY

    async def fetch_news(self, page: int = 1, page_size: int = 10) -> List[dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/everything",
                    params={
                        "q": "news",
                        "page": page,
                        "pageSize": page_size,
                        "apiKey": self.api_key,
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json().get("articles", [])
        except Exception as e:
            logger.error(f"Unexpected error fetching news: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def fetch_and_save_latest(
        self, db: Session, country_code: str = "us"
    ) -> List[News]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/top-headlines",
                    params={
                        "country": country_code,
                        "pageSize": 3,
                        "apiKey": self.api_key,
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                articles = response.json().get("articles", [])[:3]

                news_items = []
                for article in articles:
                    try:
                        news_data = NewsCreate(
                            title=article["title"],
                            description=article.get("description"),
                            url=article["url"],
                            published_at=article["publishedAt"],
                            source=article.get("source", {}).get("name"),
                            country="us",
                        )
                        news = self.create_news(db, news_data)
                        if news:
                            news_items.append(news)
                    except (KeyError, ValueError) as e:
                        logger.warning(f"Invalid article data: {str(e)}")
                        continue
                return news_items
        except Exception as e:
            logger.error(f"Unexpected error in fetch_and_save_latest: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def fetch_headlines_by_country(self, country_code: str) -> List[dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/top-headlines",
                    params={"country": country_code, "apiKey": self.api_key},
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json().get("articles", [])
        except Exception as e:
            logger.error(f"Unexpected error fetching country headlines: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def fetch_headlines_by_source(self, source_id: str) -> List[dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/top-headlines",
                    params={"sources": source_id, "apiKey": self.api_key},
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json().get("articles", [])
        except Exception as e:
            logger.error(f"Unexpected error fetching source headlines: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def fetch_headlines_filtered(
        self, country: Optional[str], source: Optional[str]
    ) -> List[dict]:
        try:
            if country and source:
                logger.warning("Both country and source provided; using source only")
                params = {"sources": source}
            elif country:
                params = {"country": country}
            elif source:
                params = {"sources": source}
            else:
                params = {}
            params["apiKey"] = self.api_key

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/top-headlines", params=params, timeout=10.0
                )
                response.raise_for_status()
                return response.json().get("articles", [])
        except Exception as e:
            logger.error(f"Unexpected error fetching filtered headlines: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def create_news(self, db: Session, news: NewsCreate) -> Optional[News]:
        try:
            existing_news = db.query(News).filter(News.url == news.url).first()
            if existing_news:
                logger.info(f"News with URL {news.url} already exists")
                return None

            db_news = News(**news.model_dump())
            db.add(db_news)
            db.commit()
            db.refresh(db_news)
            return db_news
        except IntegrityError as e:
            db.rollback()
            logger.warning(f"Integrity error creating news: {str(e)}")
            return None
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating news: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Database error while creating news"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating news: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
