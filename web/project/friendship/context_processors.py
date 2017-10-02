from friendship.models import FriendshipRequest


def friendship_requests(request):
    count = 0
    if request.user.is_authenticated == True:
       requests = FriendshipRequest.objects.requests(request.user)
       count = len(requests)
    return {'requests_count': count}
