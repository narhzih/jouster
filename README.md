# LLM Knowledge Extractor

Text analysis API that extracts structured insights using OpenAI and spaCy.

## Quick Start

```bash
# Install dependencies
uv sync

# Download spaCy model
python -m spacy download en_core_web_sm

# Set OpenAI API key
cp .env.example .env
# Edit .env with your API key

# Run server
python main.py
```

Server starts at `http://localhost:8000`

## Usage

Send text to `/analyze`:

```bash
curl -X POST http://localhost:8000/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"text": "<INSERT_TEXT>"}'
```

Returns summary, topics, sentiment, and keywords.

Check `/docs` for interactive API documentation.

## Design Notes

Built with FastAPI for async LLM calls and clean service separation. Uses OpenAI function calling for reliable structured output instead of parsing. SpaCy handles keyword extraction because it's more production-ready than NLTK.

## Trade-offs

Time constraints led to some simplifications - basic error handling, no database persistence, and minimal test coverage. Focused on core functionality over bells and whistles.