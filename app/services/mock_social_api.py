import random
from typing import Dict, Optional


class MockSocialMediaAPI:
    """Mock social media API that simulates follower count changes"""

    def __init__(self):
        self._follower_data = {}

    def get_follower_count(self, platform: str, username: str) -> int:
        """Get follower count for a social media profile"""
        key = f"{platform}:{username}"

        if key not in self._follower_data:
            # Initialize with random follower count
            self._follower_data[key] = random.randint(100, 5000)
        else:
            # Simulate follower count changes
            current = self._follower_data[key]
            change = random.randint(-50, 100)  # Can gain or lose followers
            self._follower_data[key] = max(0, current + change)

        return self._follower_data[key]

    def set_follower_count(self, platform: str, username: str, count: int):
        """Set follower count for testing purposes"""
        key = f"{platform}:{username}"
        self._follower_data[key] = count


# Global instance
mock_api = MockSocialMediaAPI()
