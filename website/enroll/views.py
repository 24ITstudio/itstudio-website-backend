
import random

from django.core.exceptions import ValidationError
from django.conf import settings
if settings.DEBUG:
    def log(*a): print(*a) # type: ignore
else:
    def log(*_): pass
from .models import VerifyCodeModel, EnrollModel
from .serializers import EnrollSerializer
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .verify_code import send_code


def gen_code() -> int:
    code = random.randint(1000, 9999)
    return code


def format_code(i: int) -> str:
    return '%04d' % i


def err_response(msg: str, status = 400):
    return Response(
        data=dict(detail=msg),
        status=status
    )

@api_view(['POST'])
def send(request: Request) -> Response:
    email = request.data.get('email', None)
    if email is None:
        return err_response("email is required but missing", status=422)
    log(email)
    obj = VerifyCodeModel.objects.filter(email=email).first()
    code = gen_code()
    def create_new():
        nonlocal obj
        try:
            obj = VerifyCodeModel.objects.create(email=email, code=format_code(code))
        except ValidationError:
            return err_response("邮箱格式错误", status=422)

    if obj is not None:
        if obj.try_remove_if_unalive():
            res = create_new()
            if res is not None:
                return res
        obj.code = code
    else:
        res = create_new()
        if res is not None:
            return res
    assert obj is not None
    obj.save()

    log(code)

    err_msg = send_code(code, [email])
    if err_msg is None:
        return Response(data={}, status=200)
    else:
        return err_response(err_msg , status=500)


class EnrollViewSet(ModelViewSet):
   queryset = EnrollModel.objects.all()
   serializer_class = EnrollSerializer
 