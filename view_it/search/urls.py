from django.urls import path

from .views import search_view

app_name = "search"
urlpatterns = [
    path("", view=search_view, name="index"),
]
