from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import main_api_view, PostView, PostAddFileView, PostCommentsView, CommentView, CommentAddFileView

router = SimpleRouter()
router.register("posts", PostView)

comment_router = SimpleRouter()
comment_router.register("comments",CommentView)

urlpatterns = [
    path("", main_api_view, name="empty_api"),
    *router.urls,
    *comment_router.urls,
    path("posts/<int:id>/add-file/", PostAddFileView.as_view(actions={'post': 'create'}), name="post_add_file"),
    path("comments/<int:id>/add-file/", CommentAddFileView.as_view(actions={'post': 'create'}), name="comment_add_file"),
    path("posts/<int:id>/comments/", PostCommentsView.as_view(actions={"get": "retrieve"}), name="post_with_comments")
]
