#!/usr/bin/env python
# coding=utf-8
import time
from db import *

from setting import *

def get_hour():
    # TIMEADD aim to get Beijing Time
    return int(time.strftime('%H'))+TIMEADD

def abs(t):
    if t<0:
        return t*-1
    else:
        return t

db=DB(DBHOST,DBUSER,DBPWD,DBNAME)
now_time=get_hour()
now_time=6
result=db.select('userinfo',{'clear_time':now_time},'uid,today_score,score')
if result!=1:
    for i in result:
        uid=i['uid']
        nowpid=i['nowpid']
        today_score=int(i['today_score'])
        sum_score=int(db.sum('task','score',{'uid':uid,'pid':nowpid})) #task socre_sum
        score=int(i['score']) #user all score
        k=(today_score-sum_score)/abs(sum_score)
        k+=1
        k*=50
        db.update('userinfo',{'score':k+score,'today_score':0},{'uid':uid})
else:
    print('no need to clear')

