from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ProfileBase(BaseModel):
    platform: str
    username: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    platform: Optional[str] = None
    username: Optional[str] = None


class Profile(ProfileBase):
    id: int
    user_id: int
    current_follower_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FollowerHistoryBase(BaseModel):
    follower_count: int


class FollowerHistory(FollowerHistoryBase):
    id: int
    profile_id: int
    recorded_at: datetime

    model_config = {"from_attributes": True}


class AlertBase(BaseModel):
    profile_id: int
    threshold: int


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    threshold: Optional[int] = None
    is_active: Optional[bool] = None


class Alert(AlertBase):
    id: int
    user_id: int
    is_active: bool
    triggered: bool
    triggered_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class ProfileWithInsights(Profile):
    follower_change_24h: int
    recent_history: List[FollowerHistory]
