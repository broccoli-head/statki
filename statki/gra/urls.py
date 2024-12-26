from django.urls import path
from . import views

app_name = "gra"

urlpatterns = [
    path('', views.lista, name="lista"),
    path('nowa/', views.nowa_gra, name='nowa_gra'),
    path('bitwa/', views.bitwa, name='bitwa')
]