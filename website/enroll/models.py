from django.db import models

# Create your models here.


class VerifyCodeModel(models.Model):
    email = models.EmailField(max_length=36, unique=True)
    # this field allows at least 0-2147483647
    code = models.PositiveIntegerField()
    send_time = models.DateTimeField(auto_now=True)
    comment = models.TextField()
