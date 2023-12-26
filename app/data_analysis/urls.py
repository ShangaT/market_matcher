from django.urls import path

from . import views
from .views import Index

urlpatterns = [
    path("", Index.index, name="index"),

    path("city/<str:city_destination>/", Index.city, name='city_url'),
    path("products/<str:city_destination>/<str:category_destination>/", Index.category, name='category_url'),
]