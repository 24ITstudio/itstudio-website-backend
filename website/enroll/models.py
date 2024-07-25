
from collections.abc import Sequence, Iterable
from datetime import timedelta, datetime, timezone
from django.db import models

EmailFieldInst = models.EmailField(
    max_length=36, unique=True, verbose_name="邮箱")

ALIVE_DURATION = timedelta(minutes=10)

CODE_HELP_TEXT = "验证码"

class VerifyCodeModel(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = CODE_HELP_TEXT
    email = EmailFieldInst
    # this field allows at least 0-2147483647
    code = models.PositiveIntegerField()
    send_time = models.DateTimeField(auto_now=True)
    # XXX: auto_now=True will add a datetime with timezone.utc
    #   a.k.a. an aware datetime
    def is_alive(self) -> bool:
        send_time = self.send_time
        ddl = datetime.now(timezone.utc) - ALIVE_DURATION
        return send_time >= ddl
    def try_remove_if_unalive(self) -> bool:
        ## returns if unalive
        res = not self.is_alive()
        if res:
            self.delete()
        return res
    def __str__(self) -> str:
        return self.email


def genIntegerChoices(ls: Sequence[str], start=0) -> Iterable['tuple[int, str]']:
    return list(zip(range(start, len(ls)+start), ls))


class EnrollStatus(tuple):
    center_len: int
    def _center_as_0_len(self) -> int:
        le = len(self)
        (quo, rem) = divmod(le, 2)
        assert rem == 1
        return quo
    def __new__(cls, iterable):
        self = super().__new__(cls, iterable)
        self.center_len = self._center_as_0_len()
        return self
    def center_index(self, item) -> int:
        return self.index(item) - self.center_len
    def get_item(self, idx: int):
        return self[idx+self.center_len]


class EnrollModel(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = "报名信息"
    # the order matters and this is symmetric
    _shedules_data = EnrollStatus((
        "未录取",
        "二审失败",
        "面试失败",
        "一审失败",
        "已报名", # idx: 0
        "一审中",
        "面试中",
        "二审中",
        "成功录取",
    ))
    @classmethod
    def progress_idx(cls, status: str) -> int:
        return cls._shedules_data.center_index(status)
    @classmethod
    def get_status_str(cls, idx: int) -> str:
        return cls._shedules_data.get_item(idx)
    schedules = genIntegerChoices(
        _shedules_data,
        -_shedules_data.center_len)
    # the order matters!
    departments = genIntegerChoices((
        "程序开发",
        "Web开发",
        "游戏开发",
        "APP开发",
        "UI设计",
    ))
    name = models.CharField(max_length=20, verbose_name="姓名")
    major = models.CharField(max_length=20, verbose_name="年级专业")
    phone = models.PositiveBigIntegerField(unique=True, verbose_name="手机号码")
    # 0..9223372036854775807  (max of int64), bigger than 11 digits
    email = EmailFieldInst
    department = models.SmallIntegerField(choices=departments, verbose_name="意向部门")
    content = models.CharField(null=True, max_length=200, verbose_name="为什么要加入爱特工作室")
    status = models.SmallIntegerField(choices=schedules, default=0, verbose_name="报名状态")

    qq = models.PositiveBigIntegerField(unique=True, null=True, name="qq", verbose_name="QQ号")

    def __str__(self):
        return self.name

    STATUS_QUERY_CAND = (
        'email', 'phone', 'qq')
    STATUS_QUERY_FUZZY_CAND = ('name',)  # name is not unique

    @classmethod
    def get_status(cls, d: dict) -> tuple[int, str]:
        key = val = ''
        for cand in cls.STATUS_QUERY_CAND:
            val = d.get(cand, None)
            if val is not None:
                key = cand
                break
        if key == '':
            for cand in cls.STATUS_QUERY_FUZZY_CAND:
                val = d.get(cand, None)
                if val is not None:
                    key = cand
                    break
            if key == '': raise KeyError("no valid item used as key to look up")
        
        item = cls.objects.get(**{key: val})  # raises error iff not only one is found.
        idx = item.status
        status = cls.get_status_str(idx)
        return (idx, status)
