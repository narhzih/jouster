from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class AnalysisMetadata(BaseModel):
    title: str | None
    topics: list[str] = Field(min_length=3, max_length=3)
    sentiment: Literal["positive", "neutral", "negative"]
    keywords: list[str] = Field(min_length=3, max_length=3)


class AnalysisResult(BaseModel):
    summary: str = Field(max_length=500)
    metadata: AnalysisMetadata
    processing_time_ms: int
    created_at: datetime