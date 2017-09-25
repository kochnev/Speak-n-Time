from django import template
from friendship.models import Friendship, FriendshipRequest

register = template.Library()


@register.assignment_tag
def are_friends(user1, user2):
    return Friendship.objects.are_friends(user1, user2)


@register.assignment_tag
def get_friendship_request_id(to_user, from_user):
    return FriendshipRequest.objects.get_friendship_request_id(to_user, from_user)

