from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category_1", views.page_1, name='page_1'),
    path("category_2", views.page_2, name='page_2'),
    path("category_3", views.page_3, name='page_3'),
    path("category_4", views.page_4, name='page_4'),
    path("category_5", views.page_5, name='page_5'),
    path("category_6", views.page_6, name='page_6'),
    path("category_7", views.page_7, name='page_7'),
    path("category_8", views.page_8, name='page_8'),
    path("category_9", views.page_9, name='page_9'),
    path("category_10", views.page_10, name='page_10'),
    path("visualization",  views.visualization, name='visualization'),
]