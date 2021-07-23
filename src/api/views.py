from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import ParseError
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.models import Post, PostFile, Comment, CommentFile
from api.serializers import PostSerializer, FileSerializer, PostWithCommentSerializer, CommentSerializer


@api_view(["GET"])
def main_api_view(request):
    """Проверка работы api"""
    return Response({"status": "ok"})


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentView(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CommentAddFileView(ViewSet):
    serializer_class = FileSerializer

    def create(self, request, id, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file_obj = request.FILES['file']
        try:
            comment_instance = Comment.objects.get(id=id)
        except:
            return Response(status=404)
        comment_file = CommentFile(file=file_obj, comment=comment_instance)
        comment_file.save()
        return Response(status=204)


class PostAddFileView(ViewSet):
    serializer_class = FileSerializer

    def create(self, request, id, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        file_obj = request.FILES['file']
        try:
            post_instance = Post.objects.get(id=id)
        except:
            return Response(status=404)
        post_file = PostFile(file=file_obj, post=post_instance)
        post_file.save()
        return Response(status=204)


class PostCommentsView(ViewSet):
    def retrieve(self, request, id=None):
        query_set = Post.objects.all()
        post = get_object_or_404(query_set, pk=id)
        serializer = PostWithCommentSerializer(post)
        return Response(serializer.data)
