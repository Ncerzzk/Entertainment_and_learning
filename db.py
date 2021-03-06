#!/usr/bin/env python
# coding=utf-8
import pymysql
import pymysql.cursors
import pymysql.err
from safe import *
from error import *

class DB(object):
    """
    if error happened in this class,function will return 1
    
    """
    def __init__(self,host,user,password,db,charset='utf8'):
        self.conn=pymysql.connect(host=host,user=user,passwd=password,db=db,charset=charset, cursorclass=pymysql.cursors.DictCursor)
        self.cur=self.conn.cursor()
        self.cur.execute("set names utf8;")

    def insert(self,table,dic):
        """
         dic is a dictionary like:
         {
         'username':hello,
         'password':1234567
         }
        """
        key=''
        value=''
        for i in dic:
            key+=i+','
            value+='\''+Safe.clear(str(dic[i]))+'\''+','
        key=key[:-1:]
        value=value[:-1:]
        sql='insert into %s(%s) values(%s);' %(table,key,value)
        stats=self.cur.execute(sql)
        self.conn.commit()
        if stats==0:
            print("error,happened when insert into table.")
            return 1

    @staticmethod
    def deal_condition(condition):
        result=''
        for i in condition:
            result+=i+'=\''+Safe.clear(str(condition[i]))+'\' and '
        return result[:-4:]

    def excute(self,sql):
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.fetchall()

    def del_one(self,table,condition):
        """
        condition is a dict like {'uid':1}
        """
        sql='delete from %s where ' % table
        condition=DB.deal_condition(condition)
        sql+=condition+';'
        stats=self.cur.execute(sql)
        self.conn.commit()
        if stats==0:
            print("error,happened when del_one")
            return 1
    
    def update(self,table,value,condition):
        """
        value and condition are dictionary
        """
        condition=DB.deal_condition(condition)
        value=DB.deal_condition(value)
        value=value.replace('and',',')
        sql='update %s set %s where %s;' % (table,value,condition)
        stats=self.cur.execute(sql)
        self.conn.commit()
        if stats==0:
            print("error,happened when update")
            return 1
        else:
            return 0


    def select(self,table,condition,need='all'):
        """
        found,return the list;
        else,return 1;
        """
        condition=DB.deal_condition(condition)
        if need=='all':
            sql='select * from %s where %s;' % (table,condition)
        else:
            sql='select %s from %s where %s;' % (need,table,condition)
        stats=self.cur.execute(sql)
        if stats==0:
            print("error,nothing found,happened when select")
            return 1
        else:
            return self.cur.fetchall()

    def sum(self,table,expression,condition):
        """
        expression="score+pid"
        """
        condition=DB.deal_condition(condition)
        sql='select sum(%s) from %s where %s;' % (expression,table,condition)
        stats=self.cur.execute(sql)
        if stats!=1:
            print("error,when sum")
            return 1
        else:
            result=self.cur.fetchone()
            result=result['sum(%s)'% expression]
            return result

    def get_id(self):
        sql='select last_insert_id();'
        stats=self.cur.execute(sql)
        if stats==0:
            print("error,nothing found,happened when select")
            return 1
        else:
            return self.cur.fetchone()['last_insert_id()']
       

    def __del__(self):
        self.cur.close()
        self.conn.close()
