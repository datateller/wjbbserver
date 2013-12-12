from django.shortcuts import render
from django.http import *
from baby.models import Baby
from knowledge.models import Knowledge
from django.contrib import auth
import json
from django.contrib.auth.models import User
from django.utils import http
from django.core import serializers
from datetime import *
# Create your views here.

def getknowl(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    number = request.GET.get('number')
    if number == None or number =="":
        number = 5
    else:
        number = int(number)
    username = http.urlsafe_base64_decode(username)
    password = http.urlsafe_base64_decode(password)
    username = username.decode()
    password = password.decode()
    user = auth.authenticate(username = username, password = password)
    response = ''
    if user is None:
        response = 'AUTH_FAILED'
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



def knowledges_encode(knowls):
    rets = []
    for knowl in knowls:
        t = {}
        tags = knowl.keyword.split(';')
        commercials = {"commericalId":0, "commericalTitle":"fake_title", "commericalLink":"www.fakecommercial.com"}
        t['knowledgeId'] = knowl.id
        t['knowledgeTitle'] = knowl.title
        t['knowledgeContent'] = knowl.content
        t['knowledgePicLink'] = ""
        t['tags'] = tags
        t['commericals'] = commercials
        rets.append(t)
    return json.dumps(rets, ensure_ascii=False)
    

