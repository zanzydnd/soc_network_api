from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import main_api_view, PostView, PostAddFileView, PostCommentsView

router = SimpleRouter()
router.register("post", PostView)

urlpatterns = [
    path("", main_api_view, name="empty_api"),
    *router.urls,
    path("post/<int:id>/add-file/", PostAddFileView.as_view(actions={'post': 'create'}), name="post_add_file"),
    path("post/<int:id>/comments/", PostCommentsView.as_view(actions={"get": "retrieve"}), name="post_with_comments")
]
