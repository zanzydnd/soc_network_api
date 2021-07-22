from rest_framework import serializers

from api.models import Post


class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, instance):
        print(len(instance.comments.all()))
        return len(instance.comments.all())

    class Meta:
        model = Post
        fields = ("id", "name", "comments_count")
