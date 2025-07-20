import pytest
from unittest.mock import patch, MagicMock
from app.tasks.follower_tasks import check_profile_followers
from app.models import Profile, Alert, FollowerHistory
from app.services.mock_social_api import mock_api


def test_check_profile_followers(db, test_user):
    # Create profile
    profile = Profile(
        user_id=test_user.id,
        platform="twitter",
        username="test_handle",
        current_follower_count=500
    )
    db.add(profile)
    db.commit()
    profile_id = profile.id

    # Mock the get_follower_count to return a fixed value
    with patch.object(mock_api, 'get_follower_count', return_value=600):
        # Mock the database session
        with patch('app.tasks.follower_tasks.SessionLocal') as mock_session:
            mock_session.return_value = db

            # Run task
            check_profile_followers(profile_id)

            # Query fresh objects to verify updates
            updated_profile = db.query(Profile).filter(Profile.id == profile_id).first()
            assert updated_profile.current_follower_count == 600

            # Verify history was created
            history = db.query(FollowerHistory).filter(
                FollowerHistory.profile_id == profile_id
            ).first()
            assert history is not None
            assert history.follower_count == 600


def test_alert_triggered(db, test_user):
    # Create profile with 900 followers
    profile = Profile(
        user_id=test_user.id,
        platform="twitter",
        username="test_handle",
        current_follower_count=900
    )
    db.add(profile)
    db.commit()
    profile_id = profile.id

    # Create alert for 1000 followers
    alert = Alert(
        user_id=test_user.id,
        profile_id=profile_id,
        threshold=1000,
        is_active=True,
        triggered=False
    )
    db.add(alert)
    db.commit()
    alert_id = alert.id

    # Mock the get_follower_count to return 1100 followers (crossing threshold)
    with patch.object(mock_api, 'get_follower_count', return_value=1100):
        with patch('app.tasks.follower_tasks.SessionLocal') as mock_session:
            mock_session.return_value = db

            # Run task
            check_profile_followers(profile_id)

            # Query fresh alert to verify it was triggered
            updated_alert = db.query(Alert).filter(Alert.id == alert_id).first()
            assert updated_alert.triggered == True
            assert updated_alert.triggered_at is not None
