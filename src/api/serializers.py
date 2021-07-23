from rest_framework import serializers

from api.models import Post, Comment, PostFile


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "text")


class PostFileSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, instance):
        return instance.file.url

    class Meta:
        model = PostFile
        fields = ("file",)


class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    post_file = PostFileSerializer(many=True, read_only=True)

    def get_comments_count(self, instance):
        return len(instance.comments.all())

    class Meta:
        model = Post
        fields = ("id", "name", "comments_count", "post_file")
        read_only_fields = ("comments_count", "post_file")


class PostWithCommentSerializer(PostSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (*PostSerializer.Meta.fields, "comments")


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
