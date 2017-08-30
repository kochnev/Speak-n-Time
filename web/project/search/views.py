from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

from .sql import search_query_text


@login_required
def search(request):
    user = request.user

    with connection.cursor() as cursor:
        query_text = search_query_text.replace('{{clause}}', '')
        cursor.execute(query_text, {'userId': user.id})
        result_rows = cursor.fetchall()

    return render(
        request,
        'search/search_result.html',
        {
            'result_rows': result_rows,
        }
    )
