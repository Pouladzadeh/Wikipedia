from django.urls import path

from . import views

app_name="Wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("anypage", views.anypage, name="anypage"),
    path("create", views.create, name="create"),
    path("editpage/<str:title>", views.editpage, name="editpage")
    ]
