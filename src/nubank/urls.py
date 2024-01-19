from django.urls import path

from . import views

urlpatterns = [
    path("summary", views.categories, name="categories"),
    path("sync", views.force_sync, name="sync"),
]
