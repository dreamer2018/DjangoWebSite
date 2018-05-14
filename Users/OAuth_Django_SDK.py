# -*- coding:utf-8 -*-

import string
import random
import urllib.request as urllib2
import urllib
from django.http import HttpResponse, HttpResponseRedirect
import http.cookiejar as cookielib
import json

VERSION = "0.1"
GET_AUTH_CODE_URL = "https://sso.xiyoulinux.org/oauth/authorize"
GET_ACCESS_TOKEN_URL = "https://sso.xiyoulinux.org/oauth/access_token"
GET_USER_INFO_URL = "https://api.xiyoulinux.org/me"

APPID = 'py_develop'
APPKEY = '$2y$10$WqIwkVhwMrs2cAPkBRyp1uEPpoP2oh1mH'
CALLBACK = 'http://localhost/apis/login/'
ERRORREPORT = True  # 是否调试.
SCOPE = 'all'


def oauth_login(request):
    # 判断是否登录，如果不存在'state'参数，则表明一定未登录
    if 'state' not in request.GET.keys():
        # 生成随机的8位字符串
        state = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        # 持久化 state ， 用于后续验证
        request.session['state'] = state
        if 'next' in request.GET.keys():
            request.session['next'] = request.GET['next']
        # 参数拼接
        request_data = {
            "response_type": "code",
            "client_id": APPID,
            "redirect_uri": urllib2.unquote(CALLBACK),
            "state": state,
            "scope": SCOPE
        }
        # 做url拼接
        login_url = combine_url(GET_AUTH_CODE_URL, request_data)
        # 重定向url
        return HttpResponseRedirect(login_url)
    else:
        # 判断state是否为伪造的，并检测code字段是否存在
        if request.session['state'] == request.GET['state'] and 'code' in request.GET.keys():
            next = None
            if 'next' in request.session.keys():
                next = request.session['next']
                request.session['next'] = None
            return oauth_callback(request, next)
        else:
            return HttpResponseRedirect(request.path)


def oauth_callback(request, next=None):
    # 获取code
    code = request.GET['code']
    # 参数拼接
    requestString = {
        "grant_type": "authorization_code",
        "client_id": APPID,
        "redirect_uri": urllib2.unquote(CALLBACK),
        "client_secret": APPKEY,
        "code": code
    }
    # url编码
    data = urllib.urlencode(requestString)
    # 定义http头部信息
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # 模拟发送POST请求
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    req = urllib2.Request(GET_ACCESS_TOKEN_URL, data, header)
    result = opener.open(req)
    # 获取返回结果
    data = result.read()
    # 将json转换为dict
    dic = eval(data)
    # 获取access_token
    access_token = dic['access_token']
    request.session['access_token'] = access_token
    request.session['login'] = True
    if next is not None:
        return HttpResponseRedirect(next)
    rtu = {
        'code': 100,
        'status': True,
        'message': 'login success'
    }
    js = json.dumps(rtu)
    return HttpResponse(js)


def get_user_info(request):
    access_token = request.session['access_token']
    data = {
        'access_token': access_token
    }
    url = combine_url(GET_USER_INFO_URL, data)
    params = urllib2.unquote(url)
    response = urllib2.urlopen(params)
    dict = json.loads(response.read())
    request.session['user'] = dict['id']
    request.session['login'] = True


# 拼接url
def combine_url(base_url=None, data=None):
    if base_url is None:
        combined = ''
    else:
        combined = base_url + '?'
    if data is None:
        return combined
    for item in data:
        combined += '%s=%s&' % (item, data[item])
    combined = combined[0:len(combined) - 1]
    return combined
