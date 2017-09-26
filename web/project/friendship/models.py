from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import  timezone
from django.core.exceptions import ValidationError
from friendship.exceptions import AlreadyFriendsError


class FriendshipRequestManager(models.Manager):
    """ Friendshiprequest manager """

    def requests(self, user):
        """ Return a list of friendship requests """
        qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(rejected__isnull=True).\
            filter(to_user=user).all()
        requests = list(qs)

        return requests


    def get_friendship_request_id(self, to_user, from_user):
        """Is there friend request between user1 and user2"""
        try:
            return FriendshipRequest.objects.select_related('from_user', 'to_user'). \
                filter(to_user=to_user, from_user=from_user).get(rejected__isnull=True).id
        except FriendshipRequest.DoesNotExist:
            return None


    def sent_requests(self, user):
        """ Return a list of friendship requests from user """
        qs = FriendshipRequest.objects.select_related('from_user', 'to_user').filter(from_user=user).all()
        requests = list(qs)

        return requests



class FriendshipManager(models.Manager):
    """ Friendship manager """

    def friends(self, user):
        """ Return a list of all friends """
        qs = Friendship.objects.select_related('from_user', 'to_user').filter(to_user=user).all()
        friends = [u.from_user for u in qs]

        return friends


    def add_friend(self, from_user, to_user, message=None):
        """ Create a friendship request """
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Users are already friends")

        if message is None:
            message = ''

        request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
        )

        if created is False:
            raise AlreadyFriendsError("Friendship already requested")

        if message:
            request.message = message
            request.save()

        return request

    def remove_friend(self, from_user, to_user):
        """ Destroy a friendship relationship """
        try:
            qs = Friendship.objects.filter(
                Q(to_user=to_user, from_user=from_user) |
                Q(to_user=from_user, from_user=to_user)
            ).distinct().all()

            if qs:
                qs.delete()
                return True
            else:
                return False
        except Friendship.DoesNotExist:
            return False

    def are_friends(self, user1, user2):
        """ Are these two users friends? """
        try:
            Friendship.objects.get(to_user=user1, from_user=user2)
            return True
        except Friendship.DoesNotExist:
            return False


# Create your models here.
class Friendship(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(User, related_name='friends')
    from_user = models.ForeignKey(User, related_name="+")
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%s is friends with #%s" % (self.to_user_id, self.from_user_id)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themeselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super(Friendship, self).save(*args, **kwargs)


class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(User, related_name='friendship_requests_received')

    message = models.TextField(blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    objects = FriendshipRequestManager()

    class Meta:
        verbose_name = 'Friendship Request'
        verbose_name_plural = 'Friendship Requests'
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%s friendship requested #%s" % (self.from_user_id, self.to_user_id)

    def accept(self):
        """ Accept this friendship request """
        relation1 = Friendship.objects.create(
            from_user=self.from_user,
            to_user=self.to_user
        )

        relation2 = Friendship.objects.create(
            from_user=self.to_user,
            to_user=self.from_user
        )

        self.delete()

    def reject(self):
        """ reject this friendship request """
        #self.rejected = timezone.now()
        #self.save()

        self.delete()

    def cancel(self):
        """ cancel this friendship request """
        self.delete()

    def mark_viewed(self):
        self.viewed = timezone.now()
        self.save()


