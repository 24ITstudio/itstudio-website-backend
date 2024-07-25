
from django.contrib import admin
from . import models


def clamp_len_with(s: str, max_len_without_suffix: int,
                   suffix: str = "...") -> str:
    le = len(s)
    add_suffix = le > max_len_without_suffix
    s = s.replace('\n', ' ')
    if add_suffix:
        res = s[:max_len_without_suffix] + suffix
    else:
        res = s
    return res

@admin.display(description="Content")
def clamped_content(obj: models.comment):
    res = clamp_len_with(obj.content, 10)
    return res


@admin.display(description="Time")
def comment_time(obj: models.comment):
    res = (obj.datetime
           .strftime('%m-%d %H:%M %z')  # MM-DD hh:mm[ [+-]HHSS[.ffffff]]
           )
    return res


@admin.register(models.comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [clamped_content, comment_time]

