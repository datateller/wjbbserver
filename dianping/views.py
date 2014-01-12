from django.shortcuts import render
from django.http import *
from baby.models import Baby
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import http
from datetime import *
import json
import base64
import sys
import hashlib
import urllib
from urllib.request import urlopen
from utils.users import *
# Create your views here.

def getblist(latitude, longitude):
    appkey = "757541619"
    secret = "ce3bfb7ed3854dfa975fdbcfa9c89e73"
    apiUrl = "http://api.dianping.com/v1/business/find_businesses"
    paramSet = []
    paramSet.append(("format", "json"))
    paramSet.append(("latitude", "31.2"))
    paramSet.append(("longitude", "121.420033"))
    paramSet.append(("limit", "20"))
    paramSet.append(("radius", "2000"))
    paramSet.append(("offset_type", "0"))
    #paramSet.append(("has_coupon", "1"))
    #paramSet.append(("has_deal", "1"))
    paramSet.append(("sort", "7"))
    paramSet.append(("category","早教中心,幼儿园,亲子游乐,亲子购物,孕产护理"))
    
    paramMap = {}
    for pair in paramSet:
        paramMap[pair[0]] = pair[1]
    
    codec = appkey
    for key in sorted(paramMap.keys()):
        codec += key + paramMap[key]
    
    codec += secret
    
    sign = (hashlib.sha1(codec.encode(encoding='utf-8')).hexdigest()).upper()
    
    url_trail = "appkey=" + appkey + "&sign=" + sign
    for pair in paramSet:
        if pair[0] == 'category':
            url_trail += "&" + pair[0] + "=" + urllib.parse.quote(pair[1])
        else:
            url_trail += "&" + pair[0] + "=" + pair[1]
    
    requestUrl = apiUrl + "?" + url_trail
    
    print(requestUrl)
    response = urlopen(requestUrl)
    encodejson = json.loads(response.read().decode('utf-8'))
    return encodejson

def getbbyid(business_id):
    appkey = "757541619"
    secret = "ce3bfb7ed3854dfa975fdbcfa9c89e73"
    apiUrl = "http://api.dianping.com/v1/business/get_single_business"
    paramSet = []
    paramSet.append(("format", "json"))
    paramSet.append(("business_id", business_id))
    paramMap = {}
    for pair in paramSet:
        paramMap[pair[0]] = pair[1]
    
    codec = appkey
    for key in sorted(paramMap.keys()):
        codec += key + paramMap[key]

    codec += secret
    
    sign = (hashlib.sha1(codec.encode(encoding='utf-8')).hexdigest()).upper()
    
    url_trail = "appkey=" + appkey + "&sign=" + sign
    for pair in paramSet:
        if pair[0] == 'category':
            url_trail += "&" + pair[0] + "=" + urllib.parse.quote(pair[1])
        else:
            url_trail += "&" + pair[0] + "=" + pair[1]
    
    requestUrl = apiUrl + "?" + url_trail
    
    response = urlopen(requestUrl)
    encodejson = json.loads(response.read().decode('utf-8'))
    return encodejson


def encodebusinessbasic(bdict):
    ret = []
    #ret['businesses'] = []
    for b in bdict['businesses']:
        retb = {}
        retb['business_id'] = b['business_id']
        retb['name'] = b['name']
        retb['address'] = b['address']
        retb['telephone'] = b['telephone']
        ret.append(retb)
    return json.dumps(ret, ensure_ascii=False)

def getbusinessbasic(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    if not DEBUG:
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
    else:
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

    if not (username and password and latitude and longitude):
        return HttpResponse('PARAM_ERROR')
    response = ''
    if user is None:
        response = 'AUTH_FAILED'
    else:
        response = encodebusinessbasic(getblist(latitude, longitude))
    return HttpResponse(response)

def encodebusiness(bdict):
    ret = {}
    ret['business_id'] = bdict['business_id']
    ret['name'] = bdict['name']
    ret['branch_name'] = bdict['branch_name']
    ret['address'] = bdict['address']
    ret['telephone'] = bdict['telephone']
    ret['city'] = bdict['city']
    ret['business_url'] = bdict['business_url']
    ret['s_photo_url'] = bdict['s_photo_url']
    ret['business_id'] = bdict['business_id']
    ret['description'] = '暂时没有相关描述'
    ret['regions'] = bdict['regions']
    ret['categories'] = bdict['categories']
    return json.dumps(ret, ensure_ascii=False)

def getbusinessbyid(request):
    (authed, username, password, user) = auth_user(request)
    if not authed or not user:
        return HttpResponse('AUTH_FAILED')
    if not DEBUG:
        id = request.POST.get('id')
    else:
        id = request.GET.get('id')
    if not (username and password and id):
        return HttpResponse('PARAM_ERROR')
    response = ''
    if user is None:
        return HttpResponse('AUTH_FAILED')
    response = encodebusiness(getbbyid(id)['businesses'][0])
    return HttpResponse(response)
