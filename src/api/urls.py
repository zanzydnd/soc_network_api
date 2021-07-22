from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import main_api_view, PostView

router = SimpleRouter()

router.register("post",PostView)



urlpatterns = [
    path("", main_api_view, name="empty_api"),
    *router.urls
]