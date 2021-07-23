from unittest import mock

from django.core.files import File
from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from api.models import Post, PostFile, Comment, CommentFile


class ApiTests(APITestCase):
    def setUp(self) -> None:
        post_test1 = Post.obects.create(name="first")
        post_test1.save()

        post_test2 = Post.obects.create(name="second")
        post_test2.save()

        img_mock = mock.MagicMock(spec=File)
        img_mock.name = "mock"

        file_post_test1 = PostFile.objects.create(file=img_mock,post=post_test1)
        file_post_test1.save()
        file_post_test2 = PostFile.objects.create(file=img_mock,post=post_test2)
        file_post_test2.save()

        comment_test1 = Comment.objects.create(text="first", post=post_test2)
        comment_test2 = Comment.objects.create(text="second", post=post_test2)
        comment_test1.save()
        comment_test2.save()

        file_comment_test1 = CommentFile.objects.create(file=img_mock,comment=comment_test1)
        file_comment_test2 = CommentFile.objects.create(file=img_mock,comment=comment_test2)
        file_comment_test1.save()
        file_comment_test2.save()

