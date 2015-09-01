# Entertainment_and_learning

idea come from http://www.zhihu.com/question/33453309#answer-19211320

going on....

API
/user/reg /user/login
(mail,password)其中密码以明文发送

/user/logout
(无参数)

/task/add
(library,taskname,taskinfo,score,[limit])
其中limit为可选,不填则为-1(即不限次数)

/task/update
(library,taskname,taskinfo,score,[limit])
其中limit为可选,不填则为-1(即不限次数)

/task/del
(tid)

/task/compelete
(tid)

/project/add
(projectname,info)

/project/update
(pid,projectname,info)

/project/del
(pid)
注意:只能删除当前登陆账号所拥有的project,否则返回错误

/project/share
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误

/project/unshare
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误

/project/change(建议用这个代替share和unshare)
(pid)
注意:只能分享当前登陆账号所拥有的project,否则返回错误
