from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


from friendship.models import Friendship, FriendshipRequest
from friendship.exceptions import AlreadyFriendsError


@login_required
def friendship_create_request(request, to_username):
    """ Create a FriendshipRequest """
    ctx = {'to_username': to_username}

    if request.method == 'POST':
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        try:
            Friendship.objects.add_friend(from_user, to_user)
        except AlreadyFriendsError as e:
            messages.add_message(request, messages.ERROR, e)

        return redirect('profile', to_username)


@login_required
def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == 'POST':
        next = request.POST.get('next')
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.accept()
        if next == 'friendship_friends_list':
            return redirect('friendship_friends_list', username=request.user.username)
        else:
            return redirect('profile', username=f_request.from_user.username)


@login_required
def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_requests_received,
            id=friendship_request_id)
        f_request.reject()
        return redirect('friendship_view_friends', username=request.user.username)


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


@login_required
def friendship_remove(request, to_username):
    """ Destroy a friendship relationship """
    if request.method == 'POST':
        next = request.POST.get('next')
        selected_user = get_object_or_404(User, username=to_username)
        Friendship.objects.remove_friend(from_user=request.user, to_user=selected_user)

        if next == 'friendship_friends_list':
            return redirect('friendship_friends_list', username=request.user.username)
        else:
            return redirect('profile', username=to_username)
   

@login_required
def friendship_friends_list(request, username):
    """ View the friends of a user """
    selected_user = get_object_or_404(User, username=username)
    list_of_friends = Friendship.objects.friends(selected_user)
    requests = FriendshipRequest.objects.requests(selected_user)

    return render(
        request,
        'friendship/friend_list.html',
        {
            'selected_user': selected_user,
            'friend_list': list_of_friends,
            'requests': requests,
        }
    )







