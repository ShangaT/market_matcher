from django.urls import path

from . import views
from .views import Index

urlpatterns = [
    path("", Index.index, name="index"),

    path("perm", Index.index_perm, name='perm'),
    path("moscow", Index.index_moscow, name='moscow'),
    path("petersburg", Index.index_petersburg, name='petersburg'),

    path("perm/category_1", views.page_1, name='page_1'),
    path("perm/category_2", views.page_2, name='page_2'),
    path("perm/category_3", views.page_3, name='page_3'),
    path("perm/category_4", views.page_4, name='page_4'),
    path("perm/category_5", views.page_5, name='page_5'),
    path("perm/category_6", views.page_6, name='page_6'),
    path("perm/category_7", views.page_7, name='page_7'),
    path("perm/category_8", views.page_8, name='page_8'),
    path("perm/category_9", views.page_9, name='page_9'),
    path("perm/category_10", views.page_10, name='page_10'),
    path("moscow/category_11", views.page_11, name='page_11'), #замороженные продукты

    path("moscow/category_1", views.page_1, name='page_1'),
    path("moscow/category_2", views.page_2, name='page_2'),
    path("moscow/category_3", views.page_3, name='page_3'),
    path("moscow/category_4", views.page_4, name='page_4'),
    path("moscow/category_5", views.page_5, name='page_5'),
    path("moscow/category_6", views.page_6, name='page_6'),
    path("moscow/category_7", views.page_7, name='page_7'),
    path("moscow/category_8", views.page_8, name='page_8'),
    path("moscow/category_9", views.page_9, name='page_9'),
    path("moscow/category_10", views.page_10, name='page_10'),
    path("moscow/category_11", views.page_11, name='page_11'),

    path("petersburg/category_1", views.page_1, name='page_1'),
    path("petersburg/category_2", views.page_2, name='page_2'),
    path("petersburg/category_3", views.page_3, name='page_3'),
    path("petersburg/category_4", views.page_4, name='page_4'),
    path("petersburg/category_5", views.page_5, name='page_5'),
    path("petersburg/category_6", views.page_6, name='page_6'),
    path("petersburg/category_7", views.page_7, name='page_7'),
    path("petersburg/category_8", views.page_8, name='page_8'),
    path("petersburg/category_9", views.page_9, name='page_9'),
    path("petersburg/category_10", views.page_10, name='page_10'),
    path("petersburg/category_10", views.page_11, name='page_11'),
]