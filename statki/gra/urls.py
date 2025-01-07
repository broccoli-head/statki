from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "gra"

urlpatterns = [
    path('', views.lista, name="lista"),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('login/', auth_views.LoginView.as_view(template_name='gra/login.html'), name='login'),
    path('wyloguj/', views.wyloguj, name='wyloguj'),
    path('nowa/', views.nowa_gra, name='nowa_gra'),
    path('bitwa/<int:gra_id>', views.bitwa, name='bitwa')
]