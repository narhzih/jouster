from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(
        min_length=10,
        max_length=50000,
        description="Text to analyze"
    )