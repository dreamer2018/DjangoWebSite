# -*- coding:utf-8 -*-

import string
import random
import urllib2
import urllib
from django.http import HttpResponse, HttpResponseRedirect
import cookielib

VERSION = "0.1"
GET_AUTH_CODE_URL = "https://sso.xiyoulinux.org/oauth/authorize"
GET_ACCESS_TOKEN_URL = "https://sso.xiyoulinux.org/oauth/access_token"
GET_USER_INFO_URL = "https://api.xiyoulinux.org/me"

APPID = 'py_develop'
APPKEY = '$2y$10$WqIwkVhwMrs2cAPkBRyp1uEPpoP2oh1mH'
CALLBACK = 'http://localhost:8000/login/'
ERRORREPORT = True  # 是否调试.
SCOPE = 'all'


def oauth_login(request):
    # 判断是否登录，如果不存在'state'参数，则表明一定未登录
    if 'state' not in request.GET.keys():
        # 生成随机的8位字符串
        state = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        # 持久化 state ， 用于后续验证
        request.session['state'] = state
        # 参数拼接
        request_data = {
            "response_type": "code",
            "client_id": APPID,
            "redirect_uri": urllib.unquote(CALLBACK),
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
            return oauth_callback(request)
        else:
            return HttpResponseRedirect(request.path)


def oauth_callback(request):
    # 获取code
    code = request.GET['code']
    # 参数拼接
    requestString = {
        "grant_type": "authorization_code",
        "client_id": APPID,
        "redirect_uri": urllib.unquote(CALLBACK),
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
    # 获取用户信息
    return get_user_info(access_token)


def get_user_info(access_token):
    data = {
        'access_token': access_token
    }
    url = combine_url(GET_USER_INFO_URL, data)
    params = urllib.unquote(url)
    response = urllib.urlopen(params)
    return HttpResponse(response.read())


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
