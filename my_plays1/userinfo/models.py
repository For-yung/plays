from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Userinfo(models.Model):
    username = models.CharField('用户名',max_length=200,null=False)
    password = models.CharField('密码',max_length=200,null=False)
    email = models.CharField('邮箱',max_length=40, null=False)
    # phone = models.CharField('手机号',max_length=15, null=False)
    time = models.DateTimeField('注册日期',default = timezone.now)
    img = models.CharField('头像',max_length=200,default="/static/images/user.jpg")
    isban = models.BooleanField('禁用',default=False,null=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'userinfo'

# 电影名称
# dyName = scrapy.Field()
# 电影评分
# dyScore = scrapy.Field()
# 电影描述
# dyDesc = scrapy.Field()
# 电影图片
# dyImg = scrapy.Field()
# 详情链接
# dyLink = scrapy.Field()

class Movie(models.Model):
    title = models.CharField('电影名',max_length=50,null=False)
    score = models.CharField(verbose_name='评分',max_length=50,null=False)
    desc = models.CharField('电影描述',max_length=200,null=False)
    img = models.CharField('图片',max_length=200,null=False)
    link = models.CharField('链接',max_length=400,null=False)
    count = models.IntegerField(verbose_name='播放次数',default=0)
    isdelete = models.BooleanField('是否删除',default=False,null=False)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movie'
        ordering = ['id']

class Tv(models.Model):
    title = models.CharField('电视名',max_length=50,null=False)
    episode = models.CharField(verbose_name='剧集',max_length=50,null=False)
    role = models.CharField('主演',max_length=200,null=False)
    img = models.CharField('图片',max_length=200,null=False)
    link = models.CharField('链接',max_length=400,null=False)
    count = models.IntegerField(verbose_name='播放次数',default=0)
    isdelete = models.BooleanField('是否删除',default=False,null=False)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tv'
        ordering = ['id']

class Video(models.Model):
    desc = models.CharField('描述',max_length=200,null=False)
    time = models.DateTimeField('时间',default = timezone.now)
    video = models.CharField('视频',max_length=300,null=False) 
    u_id = models.ForeignKey(Userinfo, on_delete=models.CASCADE, related_name="user")
    count = models.IntegerField(verbose_name='播放次数',default=0)
    isdelete = models.BooleanField('是否删除',default=False,null=False)
    def __str__(self):
        return self.desc
    
    class Meta:
        db_table = 'video'
        ordering = ['id']

class Comment(models.Model):
    desc = models.TextField(verbose_name='评论')
    time = models.DateTimeField('时间',default = timezone.now)
    v_id = models.ForeignKey(Video, on_delete=models.CASCADE)
    u_id = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    isdelete = models.BooleanField('是否删除',default=False,null=False)
    def __str__(self):
        return self.desc
    
    class Meta:
        db_table = 'comment'
        ordering = ['id']

class Reply(models.Model):
    desc = models.TextField(verbose_name="回复")
    time = models.DateTimeField('时间',default = timezone.now)
    c_id = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="reply_comment")
    u_id = models.ForeignKey(Userinfo,on_delete=models.CASCADE,related_name="reply_user")
    isdelete = models.BooleanField('是否删除',default=False,null=False)
    def __str__(self):
        return self.desc
    
    class Meta:
        db_table= 'reply'
        ordering = ['id']
