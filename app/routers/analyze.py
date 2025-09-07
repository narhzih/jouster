import asyncio
import time
from datetime import datetime

from fastapi import APIRouter, HTTPException
from openai import OpenAIError

from app.models.requests import AnalyzeRequest
from app.models.responses import AnalysisResult, AnalysisMetadata
from app.services.llm_service import llm_service
from app.services.nlp_service import nlp_service

router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post("/", response_model=AnalysisResult)
async def analyze_text(request: AnalyzeRequest) -> AnalysisResult:
    start_time = time.time()

    try:
        # llm_result = await llm_service.analyze_text(request.text)
        # keywords = await nlp_service.extract_keywords(request.text)

        llm_result, keywords = await asyncio.gather(
            llm_service.analyze_text(request.text),
            asyncio.to_thread(nlp_service.extract_keywords, request.text),
            return_exceptions=True,
        )

        print(llm_result)
        print(keywords)

        if isinstance(llm_result, Exception):
            raise llm_result
        if isinstance(keywords, Exception):
            # Fallback keywords if NLP fails
            keywords = ["content", "text", "analysis"]

        processing_time = int((time.time() - start_time) * 1000)

        metadata = AnalysisMetadata(
            title=llm_result.title,
            topics=llm_result.topics,
            sentiment=llm_result.sentiment,
            keywords=keywords[:3],  # ensure exactly 3 keywords
        )

        return AnalysisResult(
            summary=llm_result.summary,
            metadata=metadata,
            processing_time_ms=processing_time,
            created_at=datetime.utcnow(),
        )

    except OpenAIError as e:
        raise HTTPException(
            status_code=503, detail=f"LLM service unavailable: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
