
from rest_framework import serializers
from . import models

class EnrollSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(
        help_text=models.CODE_HELP_TEXT, write_only=True)
    department = serializers.CharField()
    class Meta:
        model = models.EnrollModel
        exclude = ['status']
    def validate_department(self, data: str):
        idx = -1
        if data.isdigit():
            idx = int(data)
        else:
            for (i, n) in models.EnrollModel.departments:
                if n == data:
                    idx = i
            if idx == -1:
                raise serializers.ValidationError(
                    detail=repr(data)+" is not a valid choice."
                )
        return idx
    def validate(self, attrs):
        email = attrs['email']
        obj = models.VerifyCodeModel.objects.filter(email=email).first()
        if obj is None:
            raise serializers.ValidationError(
                detail="no verfication code has been sent for your account yet",
                code=404)
        if obj.try_remove_if_unalive():
            raise serializers.ValidationError(
                detail="the verfication code for your account has been outdated",
                code=410)
        code = obj.code
        if code != attrs['code']:
            raise serializers.ValidationError(
                detail="email verification code is wrong", code=400)
        del attrs['code']
        return super().validate(attrs)
