from django.utils import timezone
from .models import UserProfile
import pytz


class TimeZoneMiddleware(object):
    """To get user's timezone"""

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        #import pdb; pdb.set_trace()

        if request.user.is_authenticated():
            user = request.user
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                user_timezone = profile.timezone
                if user_timezone:
                    timezone.activate(pytz.timezone(user_timezone))
        else:
            timezone.deactivate()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
