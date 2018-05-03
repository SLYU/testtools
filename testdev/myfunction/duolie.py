#coding=utf-8
import requests
import datetime
import time,json
import threading,random
from jsonpath_rw import jsonpath, parse
proxies = {"http": "", "https": "", }
def req(uri ,method ,**kwargs):
    "接收传参，发送请求获取服务器返回数据"
    if not kwargs.has_key("headers"):
        kwargs["headers"] = ''
    if not kwargs.has_key("parms"):
        kwargs["parms"]=''
    if method == "get":
        r = requests.get(uri, headers=kwargs["headers"], params=kwargs["parms"], proxies=proxies)
    if method == "post":
        r = requests.post(uri, headers=kwargs["headers"],data =kwargs["parms"], proxies=proxies)
    return r

def getduoliedata(uin,dict,n,*args):
    """接收前端传入多列的字段，返回多列字段值"""
    L = [uin.encode('utf8')]
    f = lambda x: x.encode('utf8') if isinstance(x,unicode) else x
    for key in args:
        jsonpath_expr = parse(key)
        L = L + [int(float(f(match.value))*n) for match in jsonpath_expr.find(dict)]
    return L

