from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.database import init_db, get_db_connection
from app.ai_model import analyze_text
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        logger.info("Database initialized")
        yield
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    finally:
        conn = get_db_connection()
        conn.close()
        logger.info("Database connection closed")

app = FastAPI(lifespan=lifespan)

class ModerationRequest(BaseModel):
    user_id: str
    text: str

class ModerationResponse(BaseModel):
    decision: str
    confidence: float
    reason: str

@app.post("/moderate", response_model=ModerationResponse)
def moderate_text(data: ModerationRequest):
    try:
        decision, confidence, reason = analyze_text(data.text)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO moderation_logs (user_id, text, decision, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.user_id, data.text, decision, confidence, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        
        return {
            "decision": decision,
            "confidence": confidence,
            "reason": reason
        }
        
    except Exception as e:
        logger.error(f"Moderation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during text moderation"
        )

@app.get("/")
async def root():
    return {
        "message": "Text Moderation API is running",
        "usage": "Send POST requests to /moderate with user_id and text",
        "docs": "Visit /docs for API documentation"
    }
