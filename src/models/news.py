from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    url = Column(String, unique=True)
    published_at = Column(DateTime, default=datetime.now(timezone.utc))
    source = Column(String, nullable=True)
    country = Column(String, nullable=True)
