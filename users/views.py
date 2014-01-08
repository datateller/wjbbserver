# Create your views here.
'''
Created on Nov 2, 2013

@author: shengeng
'''
from django.http import *
from baby.models import Baby
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from datetime import *
import json
import base64

def check_user_name(username):
    if User.objects.filter(username=username).exists():
        return "exist"
    else:
        return "available"

def register(request):

    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    
    if check_user_name(username) == "exist":
        return HttpResponse("DuplicateName")
    
    print(username)
    print(password)
    
    baby = Baby.objects.create()
    baby_name = request.POST.get('name')
    baby_height = request.POST.get('babyheight')
    baby_weight = request.POST.get('babyweight')
    baby_birthday = request.POST.get('birthday')
    baby_sex = request.POST.get('babysex')
    
    baby.name = baby_name
    baby.height = baby_height
    baby.weight = baby_weight
    baby.birthday = date.today()
    baby.sex = baby_sex
    
    user = User.objects.create_user(username = username, password = password)
    user.save()
    print(user.id)
    baby.parent_id = user.id
    print(baby.parent_id)
    baby.save()
    
    response = 'False'

    if baby is None:
        response = 'False'
    else:
        response = 'True'
    return HttpResponse(response)

def update(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    baby_height = request.POST.get('babyheight')
    baby_weight = request.POST.get('babyweight')
    baby_birthday = request.POST.get('birthday')
    baby_sex = request.POST.get('babysex')
    user = auth.authenticate(username = username, password = password)
    if user is None:
        return HttpResponse('AUTH_FAILED')
    baby = Baby.objects.get(id=user.id)
    if baby_weight:
        baby.weight = baby_weight
    if baby_height:
        baby.height = baby_height
    if baby_birthday:
        baby.birthday = baby_birthday
    if baby_sex:
        baby.sex = baby_sex
    baby.save()
    response = 'False'
    if baby is None:
        response = 'False'
    else:
        response = 'True'
    return HttpResponse(response)

#GET->POST  informationcheck->InformationCheck
def informationcheck(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    print(username)
    print(password)
    user = auth.authenticate(username = username, password = password)
    response = 'False'
    if user is None:
        response = 'False'
    else:
        response = 'True'
    print(response)
    return HttpResponse(response)
