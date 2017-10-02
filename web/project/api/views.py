from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.core import serializers

import json
# Create your views here.


def get_users(request):
    query = request.GET.get('q', None)
    users = User.objects.filter(username__icontains=query).values('id', 'username')
    users_list = list(users)
    return JsonResponse(users_list, safe=False)
