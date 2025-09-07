import asyncio
import json
from typing import Any

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config import settings


class LLMAnalysisResult(BaseModel):
    summary: str
    title: str | None
    topics: list[str]
    sentiment: str


class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.tool_def = {
            "type": "function",
            "function": {
                "name": "analyze_text",
                "description": "Analyze text and extract structured information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "1-2 sentence summary of the text",
                        },
                        "title": {
                            "type": "string",
                            "description": "Title of the text if available, or generate one",
                        },
                        "topics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 3,
                            "maxItems": 3,
                            "description": "3 key topics or themes",
                        },
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "neutral", "negative"],
                            "description": "Overall sentiment classification",
                        },
                    },
                    "required": ["summary", "title", "topics", "sentiment"],
                },
            },
        }

    async def analyze_text(self, text: str) -> LLMAnalysisResult:

        messages = [
            {
                "role": "system",
                "content": "You are an expert text analyzer. ONLY analyze the exact text provided by the user. Do NOT make up, assume, or invent any content not present in the input text. If the text is too short, meaningless, or insufficient for analysis, return 'Unable to analyze insufficient content' as the summary, 'Insufficient Content' as the title, ['insufficient', 'content', 'provided'] as topics, and 'neutral' as sentiment. Extract exactly what is present in the provided text: 1) A concise 1-2 sentence summary 2) A title (extract if present, or generate based on actual content) 3) Exactly 3 key topics or themes from the actual text 4) Overall sentiment (positive/neutral/negative) based on the actual text content.",
            },
            {"role": "user", "content": text},
        ]

        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=[self.tool_def],
            tool_choice={"type": "function", "function": {"name": "analyze_text"}},
            temperature=0.3,
        )

        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            raise ValueError("No tool calls in response")

        try:
            result = json.loads(tool_calls[0].function.arguments)
            return LLMAnalysisResult(**result)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid tool call arguments: {e}")


llm_service = LLMService()
