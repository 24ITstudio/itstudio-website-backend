from django.db import models

class comment(models.Model):
    content = models.TextField(verbose_name='评论内容', default="null")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='父评论id', default="null")
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='评论时间', default="null")
    qq = models.IntegerField(verbose_name='QQ号', default="null")
    email = models.CharField(max_length=20, verbose_name='邮箱', default="null")
