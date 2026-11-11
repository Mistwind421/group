from django.db import models
from django.contrib.auth.models import User

# 学科分类表
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="学科分类")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    def __str__(self):
        return self.name

# 知识点标签表
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="知识点标签")
    def __str__(self):
        return self.name

# 学习笔记主表
class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="笔记标题")
    content = models.TextField(verbose_name="笔记正文")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="学科分类")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="知识点标签")
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    def __str__(self):
        return self.title