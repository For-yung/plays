from django.conf.urls import url,include
from django.contrib import admin
from userinfo import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^index$', views.index,name='index'),
    url(r'register/$', views.register,name='register'),
    url(r'login$', views.login,name='login'),
    url(r'logout$',views.logout,name='logout'),
    
    url(r'genres$',views.genres,name='genres'),
    
    url(r'list$',views.list,name='list'),
   
    url(r'series$',views.series,name='series$'),
    url(r'short-codes$',views.short_codes,name='short-codes'),
    url(r'single$',views.single,name='single'),
    
    url(r'comment$',views.comment,name='comment'),
    url(r'reply$',views.reply,name='reply'),
    url(r'uploadVideo$',views.uploadVideo,name='uploadVideo'),
    url(r'count_video$',views.count_video,name='count_video'),
    url(r'delete_video$',views.delete_video,name='delete_video'),
    url(r'user$',views.user,name='user'),
    url(r'updateImg$',views.updateImg,name='updateImg'),
    url(r'delete_history$',views.delete_history,name='delete_history'),
    # 搜索页面
    url(r'search$',views.search,name='search'),
    # 处理电影，电视剧的点击播放增加
    url(r'run$',views.run,name='run'),

]