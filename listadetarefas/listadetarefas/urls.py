from django.urls import path

from listas.views import home_page

urlpatterns = [
    path('', home_page),
]
