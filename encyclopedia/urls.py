from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_page, name="new"),
    path("random/", views.random_page, name="random"),
    path("entries/<str:title>/", views.read_page, name="read"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search/", views.search, name="search")

]
