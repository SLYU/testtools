# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json,time,threading,datetime
import Queue,ast
import copy
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from forms import StressTestingForm,UploadFileForm
from testdev.myfunction.bingfa import run
from testdev.myfunction.duolie import req,getduoliedata



# Create your views here.
def index(request):
    return render(request,'index.html')

def stressTesting(request):
    if request.method == 'POST':  # 当提交表单时
        form = StressTestingForm(request.POST, request.FILES)
        method_dict = {'1': 'get', '2': 'post'}
        if form.is_valid():
            # 获取表单数据
            file_from = request.FILES['file']
            uri = form.cleaned_data['uri']
            method = method_dict[form.cleaned_data['method']]
            zhanghao = form.cleaned_data['zhanghao'].split(",")
            iparms = form.cleaned_data['parms']
            iheaders = form.cleaned_data['headers']
            pos = form.cleaned_data['pos']
            nub = form.cleaned_data['nub']
            # 处理表单数据兼容后台程序
            if len(iparms) == 0:
                parms = {}
            else:
                parms = ast.literal_eval(iparms)
            if len(iheaders) == 0:
                headers = {}
            else:
                headers = ast.literal_eval(iheaders)
            #f_to_list = list(set(file_from.readlines()))  # 读取上传文件数据
            f_to_list = file_from.readlines()
            keydata = {}
            err = []
            L_responsetime = []
            starttime = datetime.datetime.now()
            def list_iterator(L):
                """迭代器，分段读取自定义并发线程"""
                sum = len(L)
                n = 0
                while sum > n:
                    l = L[n:n + nub - 1]
                    n = n + nub - 1
                    yield l

            def run(uin, parms1, headers1):
                try:
                    r = req(uri, method, parms=parms1, headers=headers1)
                    ResponseTime = float(r.elapsed.microseconds) / 1000
                    if r.status_code != 200:
                        err.append("code!=200")
                        L_responsetime.append(ResponseTime)
                    else:
                        L_responsetime.append(ResponseTime)
                except:
                    err.append('err')

            for x in list_iterator(f_to_list):
                threads = []  # 线程池
                for a in x:
                    M = a.strip().split(',')  # 账号列的值集合
                    if pos == "1":  # 用户信息位置在header中
                        D_headers = {}
                        scookie = ';'.join(map(lambda x: x + '=%s', zhanghao))  # 格式化cookie
                        D_headers['cookie'] = scookie % tuple(M)
                        headers.update(D_headers)
                    if pos == "2":  # 用户信息位置在parms中
                        D_parms = {k: v for k, v in zip(zhanghao, M)}  # list转dict
                        parms.update(D_parms)  #
                    t = threading.Thread(target=run, args=( M[0], parms.copy(), headers.copy()))  # copy深拷贝父对象（一级目录），子对象（二级目录）不拷贝，还是引用
                    threads.append(t)
                    t.start()
                for T in threads:
                    T.join()
                print "done"
            endtime = datetime.datetime.now()
            AverageTime = "{:.3f}".format(float(sum(L_responsetime)) / float(len(L_responsetime)))  # 计算数组的平均值，保留3位小数
            usetime = str(endtime - starttime)
            hour = usetime.split(':').pop(0)
            minute = usetime.split(':').pop(1)
            second = usetime.split(':').pop(2)
            totaltime = float(hour) * 60 * 60 + float(minute) * 60 + float(second)  # 计算总的思考时间+请求时间
            qps = int(len(f_to_list) / totaltime)
            keydata["request_start_time"] = str(starttime)
            keydata["request_end_time"] = str(endtime)
            keydata["request_max_time"] = max(L_responsetime)
            keydata["request_min_time"] = min(L_responsetime)
            keydata["Average_Response_Time"] = AverageTime
            keydata["qps"] = qps
            keydata["Concurrent_processing"] = nub
            keydata["use_total_time"] = totaltime
            keydata["fail_request"] = err.count("code!=200")
            r = keydata
    else:  # 当正常访问时
        form = StressTestingForm()
        r = {}
    context = {'form':form,'r':r}
    return render(request, 'stressTesting.html',context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        method_dict = {'1': 'get', '2': 'post'}
        print '提交开始时间：',time.ctime()
        if form.is_valid():
            #获取表单数据
            file_from = request.FILES['file']
            uri = form.cleaned_data['uri']
            method = method_dict[form.cleaned_data['method']]
            zhanghao = form.cleaned_data['zhanghao'].split(",")
            tofileds = tuple(form.cleaned_data['tofileds'].split(","))
            iparms = form.cleaned_data['parms']
            iheaders = form.cleaned_data['headers']
            pos = form.cleaned_data['pos']
            floattoint = form.cleaned_data['floattoint']
            nub = form.cleaned_data['nub']
            #处理表单数据兼容后台程序
            if floattoint is None:
                floattoint =1
            if len(iparms) ==0:
                parms = {}
            else:
                parms = ast.literal_eval(iparms)
            if len(iheaders) ==0:
                headers = {}
            else:
                headers = ast.literal_eval(iheaders)
            #多列数据写入路径
            filename = str(time.time()).split('.')[0]+'.txt'
            file_abs = "D:\\autotest\\duoliebag\\"+filename
            #f_to_list = list(set(file_from.readlines()))#读取上传文件数据
            f_to_list = file_from.readlines()
            queue = Queue.Queue()# 数据队列

            def list_iterator(L):
                """迭代器，分段读取自定义并发线程"""
                sum = len(L)
                n = 0
                while sum > n:
                    l = L[n:n + nub-1]
                    n = n + nub-1
                    yield l

            def write(queue, file_abs):
                """写队列数据至文件"""
                with open(file_abs, 'a+') as file_to:
                    while True:
                        line = queue.get()
                        if line == "":
                            break
                        file_to.write(line)

            def run(queue, uin, parms1, headers1):
                #lock.acquire()
                try:
                    r = req(uri, method, parms=parms1, headers=headers1)
                    if r.status_code != 200:
                        f = lambda x: x.encode('utf8') if isinstance(x, unicode) else x
                        L_tofileds = map(lambda x:-2147483648,form.cleaned_data['tofileds'].split(","))
                        L_tofileds.insert(0,f(uin))
                        r1 = str(L_tofileds)
                        r2 = r1.strip('[').strip(']').replace('\'','').replace(' ','')
                    else:
                        r = r.json()
                        r1 = str(getduoliedata(uin, r,floattoint, *tofileds))
                        r2 = r1.strip("[").strip("]").replace('\'','').replace(' ','')
                    queue.put(r2 + '\n')
                except:
                    queue.put("err" + '\n')
                #finally:
                    #lock.release()

            def file_iterator(file_name, chunk_size=512):
                '''文件读取迭代器'''
                with open(file_name) as f:
                    while True:
                        c = f.read(chunk_size)
                        if c:
                            yield c
                        else:
                            break

            write_thread = threading.Thread(target=write, args=(queue, file_abs))
            write_thread.start()
            for x in list_iterator(f_to_list):
                threads = []  #线程池
                for a in x:
                    M = a.strip().split(',')#账号列的值集合
                    if pos == "1":#用户信息位置在header中
                        D_headers= {}
                        scookie = ';'.join(map(lambda x: x+'=%s',zhanghao))#格式化cookie
                        D_headers['cookie'] = scookie % tuple(M)
                        headers.update(D_headers)
                    if pos == "2": #用户信息位置在parms中
                        D_parms={k:v for k,v in zip(zhanghao,M)}#list转dict
                        parms.update(D_parms)#
                    t = threading.Thread(target=run, args=(queue,M[0],parms.copy(),headers.copy()))#copy深拷贝父对象（一级目录），子对象（二级目录）不拷贝，还是引用
                    threads.append(t)
                    t.start()
                for T in threads:
                    T.join()
                print "done"

            queue.put("")
            write_thread.join()
            print '文件完成时间：',time.ctime()
            response = StreamingHttpResponse(file_iterator(file_abs))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
            return response

    else:
        form = UploadFileForm()
    return render(request,'upload_file.html',{"form":form})

def test(request):
    dict = {"retCode": 0,"retInfo": "成功","data": {"callBack": "aferDmMetricApi","resultData": 0,
                                                  "rdhp": "rc20.dc.DCMETA.db:50020","rau": "redis@dc"}}
    J = json.dumps(dict)
    return HttpResponse(J)