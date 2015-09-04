#!/usr/bin/env python
# coding=utf-8
import urllib.request
import urllib.parse
import http.cookiejar

cookiejar=http.cookiejar.CookieJar()
cookiehandler=urllib.request.HTTPCookieProcessor(cookiejar)
opener=urllib.request.build_opener(cookiehandler,urllib.request.HTTPHandler)

def get(url):
    html=opener.open(url)
    return html.read().decode('utf-8')

def post(url,data=None):
    data=urllib.parse.urlencode(data)
    data=data.encode()
    html=opener.open(url,data=data)
    return html.read().decode('utf-8')

def reg(mail,pwd):
    data={
        'mail':mail,
        'password':pwd
    }
    print(post('http://localhost:8888/user/reg',data))

def login(mail,pwd):
    data={
        'mail':mail,
        'password':pwd
    }
    print(post('http://localhost:8888/user/login',data))
def addproject(projectname,info):
    data={
    'projectname':projectname,
    'info':info
    }
    print(post('http://localhost:8888/project/add',data))
def setnowpid(pid):
    data={
    'pid':pid
    }
    print(post('http://localhost:8888/project/setnowpid',data))    
def addtask(taskname,taskinfo,score,library,pid):
    data={
        'taskname':taskname,
        'taskinfo':taskinfo,
        'score':score,
        'library':library,
        'pid':pid
        }
    print(post('http://localhost:8888/task/add',data))
def deltask(tid):
    data={
    'tid':7,
    }
    print(post('http://localhost:8888/task/del',data))
def getlibrary():
    print(get('http://localhost:8888/task/getlibrary'))
def getnowtask():
    print(get('http://localhost:8888/task/getnowtask'))

login('huangzzk@bupt.edu.cn4','6789mm')
#addproject('projecttest','info_null')
#setnowpid(5)
addtask('task11111','task1info',3,'entertainment',5)
#addtask('task2','task2info',-3,'entertainment',5)
#addtask('task3','task3info',7,'entertainment',4)
getlibrary()
getnowtask()
#print(post('http://localhost:8888/logout',data))
"""
data={
    'taskname':'task_name_test',
    'taskinfo':'task_desicribe',
    'score':5,
    'library':'entertainment',
    'pid':1
    }
print(post('http://localhost:8888/task/add',data))
"""
"""
data={
    'tid':5,
    'taskname':'task_name_test',
    'taskinfo':'task_desicribe',
    'score':100,
    'library':'entertainment',
    'pid':1
    }
print(post('http://localhost:8888/updatetask',data))
"""
"""
data={
    'tid':7,
    }
print(post('http://localhost:8888/task/del',data))
"""
"""
data={
    'tid':8,
    }
print(post('http://localhost:8888/task/compelete',data))
"""
"""
data={
    'projectname':'haokun',
    'info':'xinxi!'
    }
print(post('http://localhost:8888/addproject',data))
"""
"""
data={
    'uid':25
    }
print(post('http://localhost:8888/user/get',data))

"""
