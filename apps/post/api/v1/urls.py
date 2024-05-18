from django.urls import path

from apps.post.api.v1.views import PostView

urlpatterns = [
    path('', PostView.as_view(), name='post_view'),
]
