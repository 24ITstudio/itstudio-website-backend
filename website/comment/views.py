
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import commentSerializer


class CommentView(APIView):
    def get(self, _request):
        comments = comment.objects.filter(parent=None)
        serializer = commentSerializer(comments, many=True).data
        for i in serializer:
            sub_comment = comment.objects.filter(parent=i['id'])
            i['children'] = commentSerializer(sub_comment, many=True).data
        return Response(serializer)

    def post(self, request):
        content = request.data.get("content")
        s_parent_id = request.data.get("parent")
        def create_return(parent):
            comment.objects.create(content=content, parent=parent)
            return Response({'code': 200, 'msg': '成功'}, status=200)
        if s_parent_id is None:
            return create_return(None)
        parent_id = int(s_parent_id)
        parent = comment.objects.filter(id=parent_id)
        if parent is not None:
            return create_return(parent)
        else:
            return Response({'code': 404, 'detail': 'parent_id不存在'}, status=404)
