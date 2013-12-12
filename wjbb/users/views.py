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
    user = User.objects.filter(username__exact = username)
    if user:
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
        return HttpResponse("DUPLICATE_NAME")
    
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
    if not username:
        return HttpResponse('USERNAME_CANNOT_BE_NULL')
    else:
        username = http.urlsafe_base64_decode(username)
        username = username.decode()
        
    if not User.objects.filter(username__exact = username):
        return HttpResponse('USER_NOT_EXIST')
    
    password = request.POST.get('password')
    if not password:
        return HttpResponse('PASSWORD_CANNOT_BE_NULL')
    else:
        password = http.urlsafe_base64_decode(password)
        password = password.decode()

    user = User.objects.get(username = username)
    if not user.check_password(password):
        return HttpResponse('AUTH_FAILED')

    newpassword = request.POST.get('newpassword')
    if newpassword:
        newpassword = http.urlsafe_base64_decode(newpassword)
        newpassword = newpassword.decode()
        user.set_password(newpassword)
        user.save()
        
    baby_height = request.POST.get('babyheight')
    baby_weight = request.POST.get('babyweight')
    baby_birthday = request.POST.get('birthday')
    baby_sex = request.POST.get('babysex')
    baby_name = request.POST.get('babyname')
    
    baby = Baby.objects.get(parent_id = user.id)
    if not baby:
        return HttpResponse('BABY_NOT_EXIST')
    if baby_weight:
        baby.weight = baby_weight
    if baby_height:
        baby.height = baby_height
    if baby_birthday:
        baby.birthday = baby_birthday
    if baby_sex:
        baby.sex = baby_sex
    if baby_name:
        baby.name = baby_name
    baby.save()
    return HttpResponse('True')

#GET->POST  informationcheck->InformationCheck
def informationcheck(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    user = auth.authenticate(username = username, password = password)
    response = 'False'
    if user is None:
        response = 'False'
    else:
        response = 'True'
    return HttpResponse(response)
