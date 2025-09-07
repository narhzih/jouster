# Parse Mind - LLM Text Analysis API

A FastAPI service that analyzes text using OpenAI and NLTK to extract structured insights.

## Quick Start

```bash
# Install dependencies
uv sync

# Set OpenAI API key
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Run server
python main.py
```

Server runs at `http://localhost:8000`

## Usage

POST text to analyze:

```bash
curl -X POST http://localhost:8000/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text content here..."}'
```

Returns structured analysis:
```json
{
  "summary": "Brief summary of the text",
  "metadata": {
    "title": "Generated or extracted title",
    "topics": ["topic1", "topic2", "topic3"],
    "sentiment": "positive|neutral|negative",
    "keywords": ["keyword1", "keyword2", "keyword3"]
  },
  "processing_time_ms": 1500,
  "created_at": "2025-09-07T13:24:43.123456"
}
```

Interactive docs at `/docs`

## Features

- **LLM Analysis**: OpenAI function calling for reliable structured output
- **Keyword Extraction**: NLTK for identifying most frequent nouns
- **Parallel Processing**: LLM and NLP services run concurrently
- **Error Handling**: Graceful degradation when services fail
- **Input Validation**: Prevents analysis of insufficient content

## Design Rationale

Built with FastAPI for modern async support and automatic documentation. Used OpenAI function calling instead of prompt parsing for guaranteed response structure. NLTK provides reliable keyword extraction without heavy model dependencies.

## Trade-offs

Prioritized working core functionality over comprehensive features due to time constraints. Limited error recovery, no database persistence, and basic test coverage. Focused on clean architecture that could be extended later.