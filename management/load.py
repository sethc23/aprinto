
from django.shortcuts import render
from django.contrib.auth.models import User

def new_user(request):
    user = User.objects.create_user('seth', 'seth@seth.com', 'sethpassword')
    user.save()
    return render(request, 'management/success.html', {})

