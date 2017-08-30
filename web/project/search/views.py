from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

from .sql import main_search_query_text
from main.models import UserProfile

@login_required
def search(request):
    user = request.user

    partners = UserProfile.objects.raw(main_search_query_text, {'userId': user.id})

    return render(
        request,
        'search/search_result.html',
        {
            'partners': partners,
        }
    )
