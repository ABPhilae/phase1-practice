"""
Main FastAPI application.
This is the entry point for the API server.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import logging

# ---- LOGGING SETUP ----
# Think of logging as a security camera for your restaurant.
# It records everything that happens so you can debug problems later.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---- APP CREATION ----
app = FastAPI(
    title="Phase 1 Practice API",
    description="A professional FastAPI application for practicing AI engineering skills",
    version="0.1.0",
)

# ---- DATA MODELS ----
# Pydantic models are like order forms in a restaurant.
# They define EXACTLY what information is expected.
# If a customer sends the wrong format, the order is rejected automatically.

class TextInput(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text to process"
    )
    language: str = Field(
        default="auto",
        description="Language code (e.g., en, fr) or auto for detection"
    )

class TextResponse(BaseModel):
    word_count: int
    character_count: int
    processed_at: str

# ---- ENDPOINTS ----

# Health check endpoint - EVERY production API needs this.
# It is like a heartbeat monitor for your service.
# Monitoring tools ping this to confirm the service is alive.
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/analyze", response_model=TextResponse)
async def analyze_text(input_data: TextInput):
    """Analyze text and return basic statistics."""
    logger.info(f"Received text analysis request ({len(input_data.text)} chars)")

    try:
        words = input_data.text.split()
        result = TextResponse(
            word_count=len(words),
            character_count=len(input_data.text),
            processed_at=datetime.utcnow().isoformat(),
        )
        logger.info(f"Analysis complete: {result.word_count} words")
        return result

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
