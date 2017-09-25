from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from friendship.models import Friendship, FriendshipRequest
from friendship.exceptions import AlreadyExistsError

@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.accept()
        return redirect('friendship_view_friends', username=request.user.username)

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.reject()
        return redirect('friendship_view_friends')

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)



def friendship_view_friends(request, username):
    """ View the friends of a user """
    selected_user = get_object_or_404(User, username=username)
    list_of_friends = Friendship.objects.friends(selected_user)
    requests = FriendshipRequest.objects.active_requests(selected_user)

    return render(
        request,
        'friendship/friend_list.html',
        {
            'selected_user': selected_user,
            'friend_list': list_of_friends,
            'requests': requests,
        }
    )


def friendship_request_list(request):
    """ View unread and read friendship requests """
    friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, '' ,{'requests': friendship_requests})


def friendship_request_detail(request, friendship_request_id):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, 'friendship/request_detail.html', {'friendship_request': f_request})


@login_required
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
            return redirect('profile', to_username)


@login_required
def friendship_cancel(request, friendship_request_id, to_username):
    """ Cancel a previously created friendship_request_id """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_sent,
            id=friendship_request_id)
        f_request.cancel()

    return redirect('profile', to_username)

        #return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)




