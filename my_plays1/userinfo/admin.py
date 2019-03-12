from django.contrib import admin
from .models import *

#声明 Author 的高级管理类 AuthorAdmin
class VideoAdmin(admin.ModelAdmin):
    # 1.定义在列表项上显示的属性们
    list_display = ['desc','id']
    #4.添加允许被搜索的字段们
    search_fields = ['desc','id']
    # #2.定义允许被点击的字段们
    list_display_links = ['desc']
    #7.在详情页中显示的字段以及排列的顺序

class TvAdmin(admin.ModelAdmin):
    # 1.定义在列表项上显示的属性们
    list_display = ['title','id']
    #4.添加允许被搜索的字段们
    search_fields = ['title','id']
    list_display_links = ['title']


class MovieAdmin(admin.ModelAdmin):
    # 1.定义在列表项上显示的属性们
    list_display = ['title','id']
    #2.定义允许被点击的字段们
    list_display_links = ['title']
    #4.添加允许被搜索的字段们
    search_fields = ['title','id']
    #7.在详情页中显示的字段以及排列的顺序

# Register your models here.
admin.site.register(Userinfo)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tv, TvAdmin)
admin.site.register(Movie, MovieAdmin)
