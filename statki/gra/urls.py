from django.urls import path
from . import views

app_name = "gra"

urlpatterns = [
    path('', views.lista, name="lista"),
]