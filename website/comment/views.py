
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import commentSerializer


class CommentView(APIView):
    def get(self, request):
        limit = request.data.get('limit', 20)
        if type(limit) is not int:
            return Response(dict(detail="limit is not an integer"), status=422)
        comments = comment.objects.filter(parent=None)[:limit]
        serializer = commentSerializer(comments, many=True).data
        for i in serializer:
            sub_comment = comment.objects.filter(parent=i['id'])
            i['children'] = commentSerializer(sub_comment, many=True).data
        return Response(serializer)

    def post(self, request):
        content = request.data.get("content")
        parent_id = request.data.get("parent")
        def create_return(parent):
            try:
                comment.objects.create(content=content, parent=parent)
            except IntegrityError as e:
                return Response(dict(detail=str(e)), status=422)
            else:
                return Response({}, status=200)
        if parent_id is None:
            return create_return(None)
        parent = comment.objects.filter(id=parent_id).first()
        if parent is not None:
            return create_return(parent)
        else:
            return Response(dict(detail='parent不存在'), status=404)
