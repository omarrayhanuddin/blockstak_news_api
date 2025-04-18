from pydantic import BaseModel, ConfigDict
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    description: str | None
    url: str
    source: str | None
    country: str | None


class NewsCreate(NewsBase):
    published_at: datetime


class NewsResponse(NewsBase):
    id: int
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)
