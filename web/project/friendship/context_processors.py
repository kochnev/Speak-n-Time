from friendship.models import FriendshipRequest

def friendship_requests(request):
    requests = FriendshipRequest.objects.requests(request.user)
    count = len(requests)
    return {'requests_count': count}
