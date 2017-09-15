from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
def create_message(request, username):
    user = request.user
    selected_user = get_object_or_404(User, username=username)
