from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from app.db.database import get_db
from app.models import User, Alert, Profile
from app.schemas import AlertCreate, Alert as AlertSchema, AlertUpdate
from app.api.dependencies import authenticate_user

router = APIRouter()


@router.post("/", response_model=AlertSchema)
def create_alert(
        alert: AlertCreate,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    # Verify profile belongs to user
    profile = db.query(Profile).filter(
        and_(Profile.id == alert.profile_id, Profile.user_id == current_user.id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if alert already exists
    existing_alert = db.query(Alert).filter(
        and_(
            Alert.user_id == current_user.id,
            Alert.profile_id == alert.profile_id,
            Alert.threshold == alert.threshold,
            Alert.is_active == True
        )
    ).first()

    if existing_alert:
        raise HTTPException(status_code=400, detail="Alert already exists")

    db_alert = Alert(
        user_id=current_user.id,
        profile_id=alert.profile_id,
        threshold=alert.threshold
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.get("/", response_model=List[AlertSchema])
def get_alerts(
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    return db.query(Alert).filter(Alert.user_id == current_user.id).all()


@router.get("/{alert_id}", response_model=AlertSchema)
def get_alert(
        alert_id: int,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        and_(Alert.id == alert_id, Alert.user_id == current_user.id)
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return alert


@router.put("/{alert_id}", response_model=AlertSchema)
def update_alert(
        alert_id: int,
        alert_update: AlertUpdate,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        and_(Alert.id == alert_id, Alert.user_id == current_user.id)
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(alert, field, value)

    db.commit()
    db.refresh(alert)
    return alert


@router.delete("/{alert_id}")
def delete_alert(
        alert_id: int,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        and_(Alert.id == alert_id, Alert.user_id == current_user.id)
    ).first()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted successfully"}
