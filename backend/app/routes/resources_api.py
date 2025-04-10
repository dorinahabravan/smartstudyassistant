from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.init import Topics
import json

router = APIRouter()

@router.get("/api/resources/{topic_title}")
def get_resources_for_topic(topic_title: str):
    db: Session = SessionLocal()
    topic = db.query(Topics).filter(Topics.title.ilike(topic_title)).first()
    db.close()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    try:
        resources = json.loads(topic.resources) if topic.resources else []
    except json.JSONDecodeError:
        resources = []

    return {
        "topic": topic.title,
        "resources": resources
    }
