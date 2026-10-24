# geotags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.geo_tag import GeoTag, GeoTagType
from app.api.deps import require_permission
from pydantic import BaseModel
from typing import Any, Dict

class GeoTagCreate(BaseModel):
    type: GeoTagType; latitude: float | None = None; longitude: float | None = None
    radius: float | None = None; geometry: Dict[str, Any] | None = None
    building_id: int | None = None; active: bool = True

router = APIRouter()

@router.get("/")
def list_geotags(db: Session = Depends(get_db)):
    tags = db.execute(select(GeoTag)).scalars().all()
    return [{"id": t.id, "type": t.type.value, "lat": t.latitude, "lng": t.longitude, "qr": t.qr_token} for t in tags]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("geo_tag.manage"))])
def create_geotag(payload: GeoTagCreate, db: Session = Depends(get_db)):
    tag = GeoTag(**payload.model_dump())
    db.add(tag); db.commit(); db.refresh(tag)
    return {"id": tag.id, "type": tag.type.value, "qr_token": tag.qr_token}

@router.get("/nearby")
def get_nearby_geotags(lat: float, lng: float, radius: float = 1000, db: Session = Depends(get_db)):
    # Упрощенный запрос. В продакшене использовать PostGIS/MySQL Spatial или формулу Хаверсина
    tags = db.execute(select(GeoTag).where(GeoTag.active == True)).scalars().all()
    # Фильтрация в Python для прототипа
    nearby = [t for t in tags if t.latitude and t.longitude]
    return [{"id": t.id, "lat": t.latitude, "lng": t.longitude} for t in nearby[:50]]