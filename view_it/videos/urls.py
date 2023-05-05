from django.urls import path

from .views import video_detail_view, video_update_view, video_upload_view

app_name = "videos"
urlpatterns = [
    path("upload/", view=video_upload_view, name="upload"),
    path("~update/", view=video_update_view, name="update"),
    path("<slug:url_slug>/", view=video_detail_view, name="detail"),
]
