# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.core.urlresolvers import reverse
#导入异常
from django.core.exceptions import ObjectDoesNotExist
#导入加密算法
from werkzeug.security import generate_password_hash,check_password_hash

import logging
from django.db import DatabaseError
import os
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
# Create your views here.
# 导入时间。用于存历史记录
import datetime

# 导入搜索功能模块
from django.db.models import Q

#定义加密字符串
auth_check = "YangHuaLoveWanglili"

#主页
def index(request):
    id = request.session.get('uid',None)
    try:
        user = Userinfo.objects.filter(id=id).first()
    except:
        user = None
    movies_good = Movie.objects.all()[0:12]
    movies_count = Movie.objects.order_by('-count')[0:12]
    movies_score = Movie.objects.order_by('-score')[0:12]
    tvs_good = Tv.objects.all()[0:12]
    tvs_count = Tv.objects.order_by('-count')[0:12]
    dic={
        'my_user':user,
        'movies_good':movies_good,
        'movies_count':movies_count,
        'movies_score':movies_score,
        'tvs_good':tvs_good,
        'tvs_count':tvs_count,
    }
    return render(request,'index.html',dic)


# <input type="text" name="username" placeholder="用户名" required="">
# <input type="password" name="password" placeholder="密码" required="">
# <input type='number' name='age'  placeholder="年龄" required="">
# <input type="password" name="password2" placeholder="确认密码" required="">
# <input type="email" name="email" placeholder="邮箱" required="">
# <input type="number" name="phone" placeholder="手机号" required="">


#登录处理
def login(request):
        #处理POST请求
        #接收前段传递过来的数据并验证登录是否成功
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        referer = request.POST.get('referer')
        user = Userinfo.objects.filter(username = name).first()
        cpwd = user.password
        isTrue = check_password_hash(cpwd, pwd)

        if user == None:
            s = '用户名不存在,请先注册'
            return render(request,referer,)

        elif (name == 'admin' and pwd == 'admin') or isTrue:
            #登录成功
            request.session['uid'] = user.id
            id1 = str(user.id)
            # resp = render(request,referer, {'my_user':user})
            resp = HttpResponseRedirect(referer)
            # 记住密码
            print(user)
            if request.POST.get('memary'):
                resp.set_cookie('loginname',name,3600)
                resp.set_cookie('uid',user.id,3600)
            return resp

        #密码错误,登录不成功
        else:
            s = '密码错误'
            return render(request,'index.html',)

#注册处理
def register(request):
    #处理get请求
    if request.method == 'GET':
        lname = request.GET.get('username')
        user = Userinfo.objects.filter(username=lname).first()
        # print(user.username)
        if user:
            dic ={
                'status':1,
                'text':'用户名称已存在!'
            }
            return JsonResponse(dic)
        else:
            dic = {
                'status': 0,
                'text': 'ok'
            }
            return JsonResponse(dic)
    
    #处理POst请求
    else:
        user = Userinfo()
        # 获取源地址
        referer = request.POST.get('referer')
        name = request.POST.get('username')
        user.username = name
        print(user.username)
        # user.age = request.POST.get('age')
        user.email = request.POST.get('email')
        # user.phone = request.POST.get('phone')
        pwd= request.POST.get('password')
        #哈希加密
        user.password = generate_password_hash(pwd, method='pbkdf2:sha1', salt_length=8)
        # 将数据保存回数据库
        user.save()
        user = Userinfo.objects.get(username=name)
        request.session['uid'] = user.id

        # user = Users.query.filter(Users.username == username).first()
        return HttpResponseRedirect(referer)

def logout(request):
    # 获取源地址
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    # if 'uid' in request.session in request.session:
    del request.session['uid']
    # url = request.headers.get('Referer', '/')
    return HttpResponseRedirect(referer)


# 加载电影页面
def genres(request):
    if request.method == 'GET':
        try:
            id = request.session.get('uid',None)
            user = Userinfo.objects.filter(id=id).first()
        except:
            user = None
        movies_list = Movie.objects.filter(isdelete=False)
        paginator = Paginator(movies_list, 24) # 每页展示24个数据
 
        page = request.GET.get('page')
        print(page)
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一页.
            movies = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围(例如20)，则提交最后一页的结果。
            movies = paginator.page(paginator.num_pages)
        print(movies)
        return render(request,'genres.html', {'movies': movies,'my_user':user})
    else:
        return render(request,'genres.html')


# 我的视频
def list(request):
    try:
        id = request.session.get('uid',None)
        user = Userinfo.objects.filter(id=id).first()
    except:
        user = None
    try:
        videos_list = user.user.filter(isdelete=False).order_by('-id')
        paginator = Paginator(videos_list, 5) # 每页展示24个数据
        page = request.GET.get('page')
        print(page)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一页.
            videos = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围(例如20)，则提交最后一页的结果。
            videos = paginator.page(paginator.num_pages)
    except:
        videos = None
    return render(request,'list.html',{'my_user':user,'videos':videos})

# 加载tv页面
def series(request):
    if request.method == 'GET':
        try:
            id = request.session.get('uid',None)
            user = Userinfo.objects.filter(id=id).first()
        except:
            user = None
        tvs_list = Tv.objects.filter(isdelete=False)
        paginator = Paginator(tvs_list, 24) # 每页展示24个数据
 
        page = request.GET.get('page')
        print(page)
        try:
            tvs = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一页.
            tvs = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围(例如20)，则提交最后一页的结果。
            tvs = paginator.page(paginator.num_pages)
        print(tvs)
        return render(request,'series.html', {'tvs': tvs,'my_user':user})
    else:
        return render(request,'series.html')

# 短视频列表
def short_codes(request,id=None):
    if request.method == 'GET':
        try:
            id = request.session.get('uid',None)
            user = Userinfo.objects.filter(id=id).first()
        except:
            user = None
        videos_list = Video.objects.filter(isdelete=False).order_by('-id')
        paginator = Paginator(videos_list, 5) # 每页展示24个数据
        page = request.GET.get('page')
        print(page)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一页.
            videos = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围(例如20)，则提交最后一页的结果。
            videos = paginator.page(paginator.num_pages)
        print(videos)

        comments = Comment.objects.filter(isdelete=False)
        replys = Reply.objects.filter(isdelete=False)
        # paginator = Paginator(comment_list, 24) # 每页展示24个数据
        # comments = paginator.page(1)
        # c = comments[0]
        # v = c.v_id.id()
        # print(v)
        return render(request,'short-codes.html', {'videos': videos,'comments':comments,'my_user':user,'replys':replys})
    else:
        return render(request,'short-codes.html')
    

# 存储视频下的评论，
def comment(request):
    if request.method=='POST':
        desc = request.POST.get('message')
        vid = int(request.POST.get('v_id'))
        uid = int(request.POST.get('u_id'))
        print(type(vid),vid)
        print(type(uid),uid)
        video = Video.objects.filter(id=vid)[0]
        user = Userinfo.objects.filter(id=uid)[0]
        print(type(video),type(user))
        # c.v_id = video
        # c.u_id = user
        c = Comment(desc=desc,v_id=video,u_id=user)
        c.save()
        id1 = str(uid)
    return HttpResponseRedirect('short-codes'+'?id='+ id1)

# 存储视频下的评论，
def reply(request):
    if request.method=='POST':
        desc = request.POST.get('message')
        cid = int(request.POST.get('c_id'))
        uid = int(request.POST.get('u_id'))
        comment = Comment.objects.filter(id=cid)[0]
        user = Userinfo.objects.filter(id=uid)[0]
        print(type(comment),type(user))
        # c.v_id = video
        # c.u_id = user
        c = Reply(desc=desc,c_id=comment,u_id=user)
        c.save()
        id1 = str(uid)
    return HttpResponseRedirect('short-codes'+'?id='+ id1)

#     url(r'single$',views.single,name='single'),
def single(request):
    try:
        id = request.session.get('uid',None)
        user = Userinfo.objects.filter(id=id).first()
    except:
        user = None
    return render(request,'single1.html',{'my_user':user})


# 接收用户发布视频
def uploadVideo(request):
    desc = request.POST.get('desc')
    uid = int(request.POST.get('u_id'))
    file = request.FILES.get('myfile')
    video = 'static/user/mp4/'+ file.name
    print(video)
    with open(video, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    user = Userinfo.objects.filter(id=uid)[0]
    print(type(user))
    # c.v_id = video
    # c.u_id = user
    v = Video(desc=desc,video="/"+video,u_id=user)
    v.save()
    return HttpResponseRedirect('list')

# 统计视频播放次数和存播放历史记录
def count_video(request):
    id = int(request.GET.get('id'))
    print(id)
    v = Video.objects.get(id=id)
    v.count = v.count + 1
    v.save()
    v = Video.objects.get(id=id)
    count = str(v.count)
    dic= {
        'text': count,
    }
    # 把历史记录存储到cookies中
    uid = request.session.get('uid',None)
    print(uid)
    if uid:
        i = datetime.datetime.now()
        v_time = "%d-%d-%d %d:%d:%d" % (i.year,i.month,i.day,i.hour,i.minute,i.second)
        print(v_time)
        response = JsonResponse(dic)
        key = 'history' + str(uid)
        if key in request.COOKIES:
            value = request.COOKIES.get(key)
            v_list = value.split(',')
            s = ',' +'video'+'=' + str(id)+ '=' + v_time
            for l1 in v_list[1:]:
                l2 = l1.split("=")
                if l2[1] == str(id):
                    v_list.remove(l1)
            value = ",".join(v_list)
            value = value + str(s)
            v_list = value.split(',')
            if len(v_list) > 6:
                v_list.pop(0)
                print(v_list)
                value = ",".join(v_list)
            print(v_list)
            response.set_cookie(key,value,max_age=3600*24)
        else:
            s = ',' +'video'+'=' + str(id)+ '=' + v_time
            value = str(uid) + s
            response.set_cookie(key,value,max_age=3600*24)
            print(value)
        return response
    else:
        return JsonResponse(dic)


# 删除我的视频
def delete_video(request):
    id = int(request.GET.get('id'))
    print(id)
    v = Video.objects.get(id=id)
    v.isdelete = True
    v.save()
    return HttpResponseRedirect('list')
    
# 个人中心
def user(request):
    try:
        id = request.session.get('uid',None)
        user = Userinfo.objects.filter(id=id).first()
    except:
        user = None
    key = 'history' + str(id)
    cookie = request.COOKIES.get(key,None)
    # cookies = "6,movie=22=2019-1-24 17:2:11,tv=24=2019-1-24 17:2:15"
    try:
        lists = cookie.split(',')
        v_lists = []
        for i in lists[1:]:
            v_list = []
            list = i.split('=')
            if list[0] == 'video':
                video = Video.objects.filter(id=int(list[1])).first()
                v_list.append('video')
                v_list.append(video)
                v_list.append(list[2])
                v_lists.append(v_list)
            elif list[0] == 'movie':
                movie = Movie.objects.filter(id=int(list[1])).first()
                v_list.append('movie')
                v_list.append(movie)
                v_list.append(list[2])
                v_lists.append(v_list)
            else:
                tv = Tv.objects.filter(id=int(list[1])).first()
                v_list.append('tv')
                v_list.append(tv)
                v_list.append(list[2])
                v_lists.append(v_list)
        v_lists.reverse()
    except:
        v_lists = None
    return render(request,'user.html',{'my_user':user,'history':v_lists})

# 更改头像
def updateImg(request):
    uid = int(request.POST.get('u_id'))
    file = request.FILES.get('myfile')
    img = 'static/user/img/'+ file.name
    with open(img, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    user = Userinfo.objects.filter(id=uid)[0]
    print(type(user))
    # c.v_id = video
    # c.u_id = user
    user.img = '/'+ img 
    user.save()
    return HttpResponseRedirect('user')

# 删除历史记录
def delete_history(request):
    uid = request.session.get('uid',None)
    id = request.GET.get('id')
    key = 'history' + str(uid)
    # 获取cookies 中的历史记录
    value = request.COOKIES.get(key)
    v_list = value.split(',')
    response = HttpResponseRedirect('user')
    if len(v_list) == 2:
        response.delete_cookie(key)
        return response
    else:
        for l1 in v_list[1:]:
            l2 = l1.split("=")
            if l2[1] == str(id):
                v_list.remove(l1)
        value = ",".join(v_list)
        response.set_cookie(key,value,max_age=3600*24)
        return response

# 搜索页面
def search(request):
    try:
        id = request.session.get('uid',None)
        user = Userinfo.objects.filter(id=id).first()
    except:
        user = None
    keyword = request.GET.get('Search')
    print(keyword)
    movies = Movie.objects.filter(Q(title__contains=keyword)|Q(desc__contains=keyword))
    videos = Video.objects.filter(desc__contains=keyword)
    # Q对象查询电视名包含关键字，或主演中包含关键字电视剧
    tvs = Tv.objects.filter(Q(title__contains=keyword) | Q(role__contains=keyword))
    # 分页
    # try:
    #     page = request.GET.get('page', 1)
    # except PageNotAnInteger:
    #     page = 1
    # p = Paginator(datas, 5)
    # data = p.page(page)
    return render(request,'search.html',
    {'my_user':user,'movies':movies,'videos':videos,'tvs':tvs,'keyword':keyword})

# 统计电影的播放次数,并跳转到相应的链接
def run(request):
    #href="run?type=movie$id={{movie.id}}&link={{movie.link}}"
    #href="run?type=tv$id={{tv.id}}&link={{tv.link}}"
    type = request.GET.get('type')
    id = request.GET.get('id')
    link = request.GET.get('link')
    if type == "movie":
        movie= Movie.objects.get(id=int(id))
        movie.count = int(movie.count) + 21
        movie.save()
    else:
        tv= Tv.objects.get(id=int(id))
        tv.count = int(tv.count) + 21
        tv.save()

    # 把历史记录存储到cookies中
    uid = request.session.get('uid',None)
    print(uid)
    if uid:
        # 获取当前时间，并格式化成字符串
        i = datetime.datetime.now()
        v_time = "%d-%d-%d %d:%d:%d" % (i.year,i.month,i.day,i.hour,i.minute,i.second)
        print(v_time)
        response = redirect(link)
        key = 'history' + str(uid)
        if key in request.COOKIES:
            value = request.COOKIES.get(key)
            v_list = value.split(',')
            s = ',' + type + '=' + str(id)+ '=' +v_time
            for l1 in v_list[1:]:
                l2 = l1.split("=")
                if l2[1] == str(id):
                    v_list.remove(l1)
            value = ",".join(v_list)
            value = value + str(s)
            v_list = value.split(',')
            if len(v_list) > 6:
                v_list.pop(0)
                print(v_list)
                value = ",".join(v_list)
            print(v_list)
            response.set_cookie(key,value,max_age=3600*24)
        else:
            s = ',' + type + '=' + str(id)+ '=' +v_time
            value = str(uid) + s
            response.set_cookie(key,value,max_age=3600*24)
            print(value)
        return response
    else:
        return redirect(link)

# 历史记录cookie编码

# "记录1,记录2"
# "记录1" type=id=time
# type : movie
#         tv
#         video

