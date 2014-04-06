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
from utils.users import *
import json, base64, traceback, random
import datetime,time

def check_user_name(username):
    if User.objects.filter(username=username).exists():
        return "exist"
    else:
        return "available"

def register(request):
    if not DEBUG:
        username = request.POST.get('username')
        password = request.POST.get('password')
        username = http.urlsafe_base64_decode(username)
        password = http.urlsafe_base64_decode(password)
        username = username.decode()
        password = password.decode()
    else:
        username = request.GET.get('username')
        password = request.GET.get('password')
    
    if check_user_name(username) == "exist":
        return HttpResponse("DuplicateName")
    print('user register, ' + username + password)
    baby = Baby.objects.create()
    baby_name = request.POST.get('babyname')
    baby_height = request.POST.get('babyheight')
    baby_weight = request.POST.get('babyweight')
    baby_birthday = request.POST.get('birthday')
    baby_sex = request.POST.get('babysex')
    baby_homeaddr = request.POST.get('homeaddr')
    baby_schooladdr = request.POST.get('schooladdr')
    
    baby.name = baby_name
    baby.height = baby_height
    baby.weight = baby_weight
    baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
    baby.sex = baby_sex
    baby.homeaddr = baby_homeaddr
    baby.schooladdr = baby_schooladdr
    print('user register, add a new baby %s, birthday: %s' % (baby.name, baby.birthday.strftime("%Y-%m-%d")))

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
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    if not DEBUG:
        baby_height = request.POST.get('babyheight')
        baby_weight = request.POST.get('babyweight')
        baby_birthday = request.POST.get('birthday')
        baby_sex = request.POST.get('babysex')
        baby_name = request.POST.get('babyname')
        baby_homeaddr = request.POST.get('homeaddr')
        baby_schooladdr = request.POST.get('schooladdr')
    else:
        baby_height = request.GET.get('babyheight')
        baby_weight = request.GET.get('babyweight')
        baby_birthday = request.GET.get('birthday')
        baby_sex = request.GET.get('babysex')
        baby_name = request.GET.get('babyname')
    print(user)
    baby = Baby.objects.filter(parent_id=user.id)
    print(baby)
    if not baby:
        response = 'Can not found your baby in db.'
        return HttpResponse(response)
    if baby_weight:
        baby.weight = float(baby_weight)
    if baby_height:
        baby.height = float(baby_height)
    if baby_birthday:
        baby.birthday = datetime.datetime.fromtimestamp(time.mktime(time.strptime(baby_birthday,"%Y-%m-%d")))
    print('user update, update baby info %s, birthday: %s' % (baby.name, baby_birthday))
    if baby_sex:
        baby.sex = baby_sex
    if baby_name:
        baby.name = baby_name
    if baby_homeaddr:
        baby.homeaddr = baby_homeaddr
    if baby_schooladdr:
        baby.schooladdr = baby_schooladdr
    print('user update info: ' + request.POST)
    baby.save()
    response = 'False'
    if baby is None:
        response = 'False'
    else:
        response = 'True'
    return HttpResponse(response)

#GET->POST  informationcheck->InformationCheck
def informationcheck(request):
    try:
        (authed, username, password, user) = auth_user(request)
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         username = http.urlsafe_base64_decode(username)
#         password = http.urlsafe_base64_decode(password)
#         username = username.decode()
#         password = password.decode()
#         user = auth.authenticate(username = username, password = password)
        if not user:
            return HttpResponse('False')
        else:
            return HttpResponse('True')
    except Exception as e:
        print(e)
        return HttpResponse(e)


def gethomepic(request):
    try:
        (authed, username, password, user) = auth_user(request)
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         username = http.urlsafe_base64_decode(username)
#         password = http.urlsafe_base64_decode(password)
#         username = username.decode()
#         password = password.decode()
#         user = auth.authenticate(username = username, password = password)
        if not user:
            return HttpResponse('AUTH_FAILED')
        else:
#             ret = {}
#             ret['pic'] = "hehe.com"
#             return HttpResponse(json.dumps(ret, ensure_ascii=False))
            piclink = "http://wjbb.cloudapp.net/homepic/%d.jpg"%random.randint(0,9)
            print(request.get_host())
            return HttpResponse(piclink)
    except Exception as e:
        print(e)
        return HttpResponse(e)
