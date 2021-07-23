from unittest import mock

from django.core.files import File
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Post, PostFile, Comment, CommentFile


class ApiTest(APITestCase):
    def setUp(self) -> None:
        post_test1 = Post.objects.create(id=1, name="first")
        post_test1.save()

        post_test2 = Post.objects.create(id=2, name="second")
        post_test2.save()

        img_mock = mock.MagicMock(spec=File)
        img_mock.name = "mock"

        file_post_test1 = PostFile.objects.create(id=1, file=img_mock, post=post_test1)
        file_post_test1.save()
        file_post_test2 = PostFile.objects.create(id=2, file=img_mock, post=post_test2)
        file_post_test2.save()

        comment_test1 = Comment.objects.create(id=1, text="first", post=post_test2)
        comment_test2 = Comment.objects.create(id=2, text="second", post=post_test2)
        comment_test1.save()
        comment_test2.save()

        file_comment_test1 = CommentFile.objects.create(id=1, file=img_mock, comment=comment_test1)
        file_comment_test2 = CommentFile.objects.create(id=2, file=img_mock, comment=comment_test2)
        file_comment_test1.save()
        file_comment_test2.save()

    def test_get_list_posts(self):
        response = self.client.get(reverse("post-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_list_comments(self):
        response = self.client.get(reverse("comment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_post_object(self):
        response = self.client.get(reverse("post-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], "first")
        self.assertEqual(response.data['comments_count'], 0)
        response = self.client.get(reverse("post-detail", kwargs={"pk": 2}))
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['name'], "second")
        self.assertEqual(response.data['comments_count'], 2)

    def test_get_comment_object(self):
        response = self.client.get(reverse("comment-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['text'], "first")
        response = self.client.get(reverse("comment-detail", kwargs={"pk": 2}))
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['text'], "second")

    def test_put_post_object(self):
        response = self.client.put(reverse("post-detail", kwargs={"pk": 1}), data={"name": "first-put"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse("post-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data['name'], "first-put")

    def test_put_comment_object(self):
        response = self.client.put(reverse("comment-detail", kwargs={"pk": 1}), data={"text": "first-put"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse("comment-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data['text'], "first-put")

    def test_create_post_object(self):
        response = self.client.post(reverse("post-list"), data={"name": "third"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_object(self):
        response = self.client.post(reverse("comment-list"), data={"text": "third", "post": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_post_object(self):
        response = self.client.delete(reverse("post-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse("post-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_object(self):
        response = self.client.delete(reverse("comment-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse("comment-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_file_post(self):
        img_mock = mock.MagicMock(spec=File)
        img_mock.name = "mock1"
        response = self.client.post(reverse("post_add_file",kwargs={"id":2}), data={"file": img_mock})
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Post.objects.get(id=2).post_file.all()),2)

    def test_add_file_comment(self):
        img_mock = mock.MagicMock(spec=File)
        img_mock.name = "mock2"
        response = self.client.post(reverse("comment_add_file", kwargs={"id": 2}), data={"file": img_mock})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Comment.objects.get(id=2).comment_file.all()), 2)