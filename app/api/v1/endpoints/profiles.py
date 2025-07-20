from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List
from app.db.database import get_db
from app.models import User, Profile, FollowerHistory
from app.schemas import ProfileCreate, Profile as ProfileSchema, ProfileWithInsights, ProfileUpdate
from app.api.dependencies import authenticate_user

router = APIRouter()


@router.post("/", response_model=ProfileSchema)
def create_profile(
        profile: ProfileCreate,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    db_profile = db.query(Profile).filter(
        and_(
            Profile.user_id == current_user.id,
            Profile.platform == profile.platform,
            Profile.username == profile.username
        )
    ).first()

    if db_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    db_profile = Profile(
        user_id=current_user.id,
        platform=profile.platform,
        username=profile.username
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/", response_model=List[ProfileSchema])
def get_profiles(
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    return db.query(Profile).filter(Profile.user_id == current_user.id).all()


@router.get("/{profile_id}", response_model=ProfileSchema)
def get_profile(
        profile_id: int,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        and_(Profile.id == profile_id, Profile.user_id == current_user.id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile


@router.put("/{profile_id}", response_model=ProfileSchema)
def update_profile(
        profile_id: int,
        profile_update: ProfileUpdate,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        and_(Profile.id == profile_id, Profile.user_id == current_user.id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


@router.delete("/{profile_id}")
def delete_profile(
        profile_id: int,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        and_(Profile.id == profile_id, Profile.user_id == current_user.id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}


@router.get("/{profile_id}/insights", response_model=ProfileWithInsights)
def get_profile_insights(
        profile_id: int,
        current_user: User = Depends(authenticate_user),
        db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        and_(Profile.id == profile_id, Profile.user_id == current_user.id)
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get follower history for the last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_history = db.query(FollowerHistory).filter(
        and_(
            FollowerHistory.profile_id == profile_id,
            FollowerHistory.recorded_at >= yesterday
        )
    ).order_by(FollowerHistory.recorded_at.desc()).limit(10).all()

    # Calculate follower change in last 24 hours
    oldest_record = db.query(FollowerHistory).filter(
        and_(
            FollowerHistory.profile_id == profile_id,
            FollowerHistory.recorded_at >= yesterday
        )
    ).order_by(FollowerHistory.recorded_at).first()

    follower_change_24h = 0
    if oldest_record:
        follower_change_24h = profile.current_follower_count - oldest_record.follower_count

    return ProfileWithInsights(
        **profile.__dict__,
        follower_change_24h=follower_change_24h,
        recent_history=recent_history
    )
