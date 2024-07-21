
from datetime import timedelta, datetime, timezone
from django.db import models

EmailFieldInst = models.EmailField(
    max_length=36, unique=True, verbose_name="邮箱")

DELTA = timedelta(minutes=10)

class VerifyCodeModel(models.Model):
    email = EmailFieldInst
    # this field allows at least 0-2147483647
    code = models.PositiveIntegerField()
    send_time = models.DateTimeField(auto_now=True)
    # XXX: auto_now=True will add a datetime with timezone.utc
    #   a.k.a. an aware datetime
    def is_alive(self) -> bool:
        send_time = self.send_time
        ddl = datetime.now(timezone.utc) - DELTA
        return send_time >= ddl
    def try_remove_if_unalive(self) -> bool:
        ## returns if unalive
        res = not self.is_alive()
        if res:
            self.delete()
        return res
    def __str__(self) -> str:
        return self.email

def genIntegerChoices(ls, start=0):
    return list(zip(range(start, len(ls)+start), ls))

class EnrollModel(models.Model):
    class Meta:
        verbose_name_plural = "报名信息"

    schedules = genIntegerChoices([
        "已报名",
        "一审中",
        "面试中",
        "二审中",
        "成功录取",
        "一审失败",
        "面试失败",
        "二审失败",
        "未录取",
    ])
    departments = genIntegerChoices([
        "程序开发",
        "Web开发",
        "游戏开发",
        "APP开发",
        "UI设计",
    ])
    name = models.CharField(max_length=20, verbose_name="姓名")
    major = models.CharField(max_length=20, verbose_name="年级专业")
    phone = models.PositiveBigIntegerField(unique=True, verbose_name="手机号码")
    # 0..9223372036854775807  (max of int64), bigger than 11 digits
    email = EmailFieldInst
    department = models.SmallIntegerField(choices=departments, verbose_name="意向部门")
    content = models.CharField(max_length=200, verbose_name="为什么要加入爱特工作室")
    status = models.SmallIntegerField(choices=schedules, default=0, verbose_name="报名状态")

    qq = models.PositiveBigIntegerField(unique=True, null=True)  # Optional QQ number

    def __str__(self):
        return self.name
