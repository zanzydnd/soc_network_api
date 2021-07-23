from django.db import models


class Post(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "post"

def post_file_path(instance, filename):
    return "post_{0}/{1}".format(instance.post.id, filename)


class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_file")
    file = models.FileField(upload_to=post_file_path)

    class Meta:
        db_table = "post_file"

class Comment(models.Model):
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        db_table = "comment"

def comment_file_path(instance, filename):
    return "comment_{0}/{1}".format(instance.comment.id, filename)


class CommentFile(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_file")
    file = models.FileField(upload_to=comment_file_path)

    class Meta:
        db_table = "comment_file"