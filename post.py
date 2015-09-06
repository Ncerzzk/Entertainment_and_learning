#!/usr/bin/env python
# coding=utf-8
import urllib.request
import urllib.parse
import http.cookiejar

LOCALHOST='http://localhost:8888/'
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
def test():
    data={'a':''}
    print(post('http://localhost:8888/test',data))
def login(mail,pwd):
    data={
        'mail':mail,
        'password':pwd
    }
    print(post('http://localhost:8888/user/login',data))

def update(username,info,clear_time,nowpid,password=None):
    data={
        'username':username,
        'info':info,
        'clear_timet':clear_time,
        'nowpid':nowpid
    }
    if password !=None:
        data['password']=password
    print(post(LOCALHOST+"user/update"))


def addproject(projectname,info):
    data={
    'projectname':projectname,
    'info':info
    }
    print(post('http://localhost:8888/project/add',data))
def delproject(pid):
    data={
        'pid':pid
        }
    print(post('http://localhost:8888/project/del',data))
def updateproject(pid,projectname,info):
    data={
        'pid':pid,
        'projectname':projectname,
        'info':info
    }
    print(post('http://localhost:8888/project/update',data))
def shareproject(pid):
    data={
        'pid':pid
        }
    print(post('http://localhost:8888/project/share',data))
def unshareproject(pid):
    data={
        'pid':pid
        }
    print(post('http://localhost:8888/project/unshare',data))
def changeshareproject(pid):
    data={
        'pid':pid
        }
    print(post('http://localhost:8888/project/change',data))
def getproject(pid):
    data={
        'pid':pid
        }
    print(post('http://localhost:8888/project/get',data))
def getallproject():
    print(get('http://localhost:8888/project/getall'))
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
def updatetask(tid,taskname,taskinfo,score,library,pid):
    data={
        'tid':tid,
        'taskname':taskname,
        'taskinfo':taskinfo,
        'score':score,
        'library':library,
        'pid':pid
        }
    print(post('http://localhost:8888/task/update',data))
def deltask(tid):
    data={
        'tid':tid
    }
    print(post('http://localhost:8888/task/del',data))
def compeletetask(tid):
    data={
        'tid':tid
    }
    print(post('http://localhost:8888/task/compelete',data))
def gettask(tid):
    data={
        'tid':tid
    }
    print(post('http://localhost:8888/task/get',data))

def getlibrary():
    print(get('http://localhost:8888/task/getlibrary'))
def getnowtask():
    print(get('http://localhost:8888/task/getnowtask'))


login('e.255mail@gmail.com','6789mm')
#login('huangzzk@bupt.edu.cn4','6789mm')
#addproject('工程测试1','这是一段测试用的信息,没多大用处.但是我想尽量多写一些东西,来测试占用.编不下去了好累.')
#updateproject(1,'工程测试1','我把废话删除了.')
getallproject()
#getproject(1)
#changeshareproject(1)
#unshareproject(1)
#setnowpid(1)
#updatetask(4,'任务测试1312321321321','task1info',3,'成就库',1)
#addtask('任务测试2','task2info',-3,'娱乐库',1)
#addtask('tasktest3','task3info',7,'成就库',1)
#gettask(4)
#deltask(6)
#compeletetask(5)
#getlibrary()
#getnowtask()
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
