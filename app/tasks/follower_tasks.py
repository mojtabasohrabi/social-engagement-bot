from celery import shared_task
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from app.db.database import SessionLocal
from app.models import Profile, FollowerHistory, Alert
from app.services.mock_social_api import mock_api
from app.services.telegram_service import telegram_service

logger = logging.getLogger(__name__)


@shared_task
def check_profile_followers(profile_id: int):
    """Check follower count for a specific profile"""
    db = SessionLocal()
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            logger.error(f"Profile {profile_id} not found")
            return

        # Get current follower count from mock API
        new_follower_count = mock_api.get_follower_count(
            profile.platform,
            profile.username
        )

        # Record history
        history = FollowerHistory(
            profile_id=profile.id,
            follower_count=new_follower_count
        )
        db.add(history)

        # Update profile
        old_count = profile.current_follower_count
        profile.current_follower_count = new_follower_count

        # Check alerts
        alerts = db.query(Alert).filter(
            Alert.profile_id == profile.id,
            Alert.is_active == True,
            Alert.triggered == False
        ).all()

        for alert in alerts:
            if old_count < alert.threshold <= new_follower_count:
                alert.triggered = True
                alert.triggered_at = datetime.utcnow()

                # Send notification
                message = f"🎉 Milestone reached! @{profile.username} on {profile.platform} has reached {alert.threshold} followers!"

                logger.info(f"Alert triggered for profile {profile.username}: {message}")

        db.commit()
        logger.info(f"Updated profile {profile.username}: {old_count} -> {new_follower_count}")

    except Exception as e:
        logger.error(f"Error checking profile {profile_id}: {e}")
        db.rollback()
    finally:
        db.close()


@shared_task
def check_all_profiles():
    """Check all active profiles for follower updates"""
    db = SessionLocal()
    try:
        profiles = db.query(Profile).all()
        for profile in profiles:
            check_profile_followers.delay(profile.id)

        logger.info(f"Scheduled checks for {len(profiles)} profiles")
    except Exception as e:
        logger.error(f"Error scheduling profile checks: {e}")
    finally:
        db.close()
