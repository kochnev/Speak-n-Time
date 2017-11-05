
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from main.models import Language


import json
# Create your views here.


def get_users(request):
    query = request.GET.get('q', None)
    users = User.objects.filter(username__icontains=query).values('id', 'username')
    users_list = list(users)
    return JsonResponse(users_list, safe=False)

def get_languages(request):
    query = request.GET.get('q', None)
    languages = Language.objects.filter(name__icontains=query).values('id', 'name')
    languages_list = list(languages)
    return JsonResponse(languages_list, safe=False)