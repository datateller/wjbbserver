from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import Knowledge
from django.contrib import auth
import json, random
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from datetime import *
import base64

# Create your views here.

def getknowllist(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    
    number = request.POST.get('number')
    if number == None or number =="":
        number = 5
    else:
        number = int(number)
#     username = http.urlsafe_base64_decode(username)
#     password = http.urlsafe_base64_decode(password)
#     username = username.decode()
#     password = password.decode()
    user = auth.authenticate(username = username, password = password)
    response = ''
    if user is None:
        response = 'Auth False'
    else:
        baby = Baby.objects.get(parent_id=user.id)
        age= int((date.today() - baby.birthday).days)
        
        knowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
        count = knowls.count()
        
        if number >= count:
            response = knowledges_encode(list(knowls))
        else:
            import random
            response = knowledges_list_encode(random.sample(list(knowls), number))
    return HttpResponse(response)

def knowledges_list_encode(knowls):
    rets = []
    for knowl in knowls:
        t = {}
        tags = knowl.keyword.split(';')
        t['knowledgeId'] = knowl.id
        t['knowledgeTitle'] = knowl.title
        import random
        t['pic'] = 'http://xzh2.cloudapp.net/pic/'+str(random.randint(0,9))+'.jpg' 
        t['icon'] = 'http://xzh2.cloudapp.net/icon/'+str(random.randint(0, 9))+'.gif'
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)

def getknowlbyid(request):
    knowlid = request.POST.get('knowledgeid')
    if not knowlid:
        return HttpResponse('ID_NULL')
    knowledge = Knowledge.objects.get(id=knowlid)
    if not knowledge:
        return HttpResponse('NOT_FOUND')
    response = knowledge_encode(knowledge)
    return HttpResponse(response)

def getknowl(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    
    number = request.POST.get('number')
    if number == None or number =="":
        number = 5
    else:
        number = int(number)
    user = auth.authenticate(username = username, password = password)
    response = ''
    if user is None:
        response = 'Auth False'
    else:
        baby = Baby.objects.get(parent_id=user.id)
        age= int((date.today() - baby.birthday).days)
        
        knowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
        count = knowls.count()
        
        if number >= count:
            response = knowledges_encode(list(knowls))
        else:
            response = knowledges_encode(random.sample(list(knowls), number))
    return HttpResponse(response)


def knowledge_encode(knowl):
    t = {}
    tags = knowl.keyword.split(';')
    commercials = [{"commericalId":0, "commericalTitle":"fake_title", "commericalLink":"www.fakecommercial.com"}]
    t['knowledgeId'] = knowl.id
    t['knowledgeTitle'] = knowl.title
    t['knowledgeContent'] = knowl.content
    t['knowledgePicLink'] = ""
    t['tags'] = tags
    t['commericals'] = commercials
    return json.dumps(t, ensure_ascii=False)

def knowledges_encode(knowls):
    rets = []
    for knowl in knowls:
        t = {}
        tags = knowl.keyword.split(';')
        commercials = [{"commericalId":0, "commericalTitle":"fake_title", "commericalLink":"www.fakecommercial.com"}]
        t['knowledgeId'] = knowl.id
        t['knowledgeTitle'] = knowl.title
        t['knowledgeContent'] = knowl.content
        t['knowledgePicLink'] = ""
        t['tags'] = tags
        t['commericals'] = commercials
        t['icon'] = "http://xzh2.cloudapp.net/icon/" + str(random.randint(0,9)) + ".png"
        t['pic'] = "http://xzh2.cloudapp.net/pic/" + str(random.randint(0,9)) + ".jpg"
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)
    

