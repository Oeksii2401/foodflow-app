
# ============================================================
# app/routers/delivery_zone.py
# ============================================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
 
from app.db.session import get_db
from app.models.delivery_zone import DeliveryZone
from app.schemas.delivery_zone import DeliveryZoneCreate, DeliveryZoneUpdate, DeliveryZoneRead
from app.core.deps import get_current_active_user
from app.models.user import User
 
router = APIRouter(prefix="/cafes/{cafe_id}/delivery-zones", tags=["delivery-zones"])
 
 
@router.get("/", response_model=list[DeliveryZoneRead])
def list_zones(cafe_id: int, db: Session = Depends(get_db)):
    return db.query(DeliveryZone).filter(DeliveryZone.cafe_id == cafe_id).all()
 
 
@router.post("/", response_model=DeliveryZoneRead, status_code=status.HTTP_201_CREATED)
def create_zone(
    cafe_id: int,
    data: DeliveryZoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    zone = DeliveryZone(**data.model_dump(), cafe_id=cafe_id)
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone
 
 
@router.patch("/{zone_id}", response_model=DeliveryZoneRead)
def update_zone(
    cafe_id: int,
    zone_id: int,
    data: DeliveryZoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    zone = db.query(DeliveryZone).filter(
        DeliveryZone.id == zone_id, DeliveryZone.cafe_id == cafe_id
    ).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(zone, field, value)
    db.commit()
    db.refresh(zone)
    return zone
 
 
@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_zone(
    cafe_id: int,
    zone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    zone = db.query(DeliveryZone).filter(
        DeliveryZone.id == zone_id, DeliveryZone.cafe_id == cafe_id
    ).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    db.delete(zone)
    db.commit()
 