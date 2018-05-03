#coding=utf-8
import requests
import datetime
import time,json
import threading,random
proxies = {"http": "", "https": "", }

class url_request:
    times = []
    error = []
    def req(self,uri,method,**kwargs):
        "接收传参，发送请求获取服务器返回数据"
        myreq=url_request()
        if not kwargs.has_key("headers"):
            kwargs["headers"] = ''
        if not kwargs.has_key("parms"):
            kwargs["parms"]=''
        if method == "get":
            r = requests.get(uri,headers=kwargs["headers"],params=kwargs["parms"],proxies=proxies)
        if method =="post":
            r = requests.post(uri,headers=kwargs["headers"],data=kwargs["parms"],proxies=proxies)
        ResponseTime=float(r.elapsed.microseconds)/1000 #获取响应时间，单位ms
        myreq.times.append(ResponseTime) #将响应时间写入数组
        if r.status_code !=200 :
            myreq.error.append("code!=200")

def run(nub,uri,method,**kwargs):
    myreq=url_request()
    threads = []
    keydata = {}
    starttime = datetime.datetime.now()
    nub = nub#设置并发线程数
    uri =uri
    method = method
    kwargs = kwargs
    for i in range(1, nub+1):
        t = threading.Thread(target=myreq.req, args=(uri, method),kwargs=kwargs)
        threads.append(t)
    for t in threads:
        #t.setDaemon(True)
        t.start()
    t.join()
    endtime = datetime.datetime.now()
    AverageTime = "{:.3f}".format(float(sum(myreq.times))/float(len(myreq.times))) #计算数组的平均值，保留3位小数
    usetime = str(endtime - starttime)
    hour = usetime.split(':').pop(0)
    minute = usetime.split(':').pop(1)
    second = usetime.split(':').pop(2)
    totaltime = float(hour)*60*60 + float(minute)*60 + float(second) #计算总的思考时间+请求时间
    qps = int(nub/totaltime)
    keydata["request_start_time"] = str(starttime)
    keydata["request_end_time"] = str(endtime)
    keydata["request_max_time"] = max(myreq.times)
    keydata["request_min_time"] = min(myreq.times)
    keydata["Average_Response_Time"] = AverageTime
    keydata["qps"] = qps
    keydata["Concurrent_processing"] = nub
    keydata["use_total_time"] = totaltime
    keydata["fail_request"] = myreq.error.count("code!=200")
    print json.dumps(keydata,indent=3)
    return keydata

