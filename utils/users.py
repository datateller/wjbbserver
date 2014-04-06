'''
Created on 2014年1月12日

@author: shengeng
'''

DEBUG = False

from django.http import *
from baby.models import Baby
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from datetime import *
import json, base64

def auth_user(request):
    print('begin to auth')
    if not DEBUG:
        print('begin to auth')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username from POST is ' + username)
        print('password from POST is ' + password)
        username = http.urlsafe_base64_decode(username)
        password = http.urlsafe_base64_decode(password)
        username = username.decode()
        password = password.decode()
    else:
        username = request.GET.get('username')
        password = request.GET.get('password')
        print(username)
        print(password)
    user = auth.authenticate(username = username, password = password)
    if user is None:
        return(False, username, password, user)
    else:
        return(True, username, password, user)
