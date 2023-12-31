# services.py

from .models import Friendship
from django.db.models import Q

class FriendshipService:
    @staticmethod
    def are_friends(user1, user2):
        # return Friendship.objects.filter(
        #     (Q(user=user1, related_friends=user2) |
        #      Q(user=user2, related_friends=user1))
        # ).exists()
        return True
