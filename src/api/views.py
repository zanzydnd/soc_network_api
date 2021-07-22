from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Post
from api.serializers import PostSerializer


@api_view(["GET"])
def main_api_view(request):
    """Проверка работы api"""
    return Response({"status": "ok"})


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()