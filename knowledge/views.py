from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from datetime import *
from utils.users import *
import base64, json, random

# Create your views here.

def getknowllist(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    number = request.POST.get('number')
    if number == None or number =="":
        number = 5
    else:
        number = int(number)
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
        t['pic'] = 'http://xzh2.cloudapp.net/pic/'+str(random.randint(0,9))+'.jpg'
        t['icon'] = 'http://xzh2.cloudapp.net/icon/'+str(random.randint(0, 9))+'.png'
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)

def getknowlbyid(request):
    knowlid = request.GET.get('knowledgeid')
    if not knowlid:
        return HttpResponse('ID_NULL')
    knowledge = Knowledge.objects.get(id=knowlid)
    if not knowledge:
        return HttpResponse('NOT_FOUND')
    response = knowledge_encode(knowledge)
    return HttpResponse(response)

def getknowl(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    number = request.POST.get('number')
    if number == None or number =="":
        number = 5
    else:
        number = int(number)
#     username = http.urlsafe_base64_decode(username)
#     password = http.urlsafe_base64_decode(password)
#     username = username.decode()
#     password = password.decode()
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
        
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)
    

def collectknowl(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    knowlid = request.POST.get('id')
    if knowlid == None or knowlid =="":
        return HttpResponse('NULL_ID')
    try:
        collection_record = KnowledgeCollection.objects.get(user_id = user.id)
    except KnowledgeCollection.DoesNotExist:
        new_collection_record = KnowledgeCollection.objects.create()
        new_collection_record.user_id = user.id
        new_collection_record.collection_list = '|%s|' % knowlid
        new_collection_record.save()
        return HttpResponse('True')
    else:
        collection_list = collection_record.collection_list
        if collection_list.find('|%s|'%knowlid) < 0:
            collection_record.collection_list = '%s%s|'%(collection_list,knowlid)
            collection_record.save()
        return HttpResponse('True')


