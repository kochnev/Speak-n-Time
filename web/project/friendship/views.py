from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from friendship.models import Friendship, FriendshipRequest
from friendship.exceptions import AlreadyExistsError


# Create your views here.
def friend_list(request):
    pass


def friendship_create_request(request, to_username):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username}

    if request.method == 'POST':
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        try:
            Friendship.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            ctx['errors'] = ["%s" % e]
        else:
            return redirect('profile', request.user.username)

    return render(request, 'friendship/create_request.html', ctx)





