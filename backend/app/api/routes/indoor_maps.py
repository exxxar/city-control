# indoor_maps.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.map_layer import MapLayer
from app.models.map_zone import MapZone
from app.api.deps import require_permission
from pydantic import BaseModel
from typing import Any, Dict

class LayerCreate(BaseModel):
    name: str; building_id: int; file_url: str; bounds: Dict[str, Any] | None = None

class ZoneCreate(BaseModel):
    name: str; map_layer_id: int; geometry: Dict[str, Any]

router = APIRouter()

@router.get("/")
def list_layers(db: Session = Depends(get_db)):
    layers = db.execute(select(MapLayer)).scalars().all()
    return [{"id": l.id, "name": l.name, "building_id": l.building_id} for l in layers]

@router.post("/", status_code=201, dependencies=[Depends(require_permission("indoor_map.manage"))])
def create_layer(payload: LayerCreate, db: Session = Depends(get_db)):
    layer = MapLayer(**payload.model_dump())
    db.add(layer); db.commit(); db.refresh(layer)
    return {"id": layer.id, "name": layer.name}

@router.get("/{layer_id}/zones")
def get_zones(layer_id: int, db: Session = Depends(get_db)):
    zones = db.execute(select(MapZone).where(MapZone.map_layer_id == layer_id)).scalars().all()
    return [{"id": z.id, "name": z.name, "geometry": z.geometry} for z in zones]

@router.post("/{layer_id}/zones", status_code=201, dependencies=[Depends(require_permission("indoor_map.manage"))])
def create_zone(layer_id: int, payload: ZoneCreate, db: Session = Depends(get_db)):
    zone = MapZone(map_layer_id=layer_id, **payload.model_dump(exclude={"map_layer_id"}))
    db.add(zone); db.commit(); db.refresh(zone)
    return {"id": zone.id, "name": zone.name}