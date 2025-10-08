from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name = "home"),
    path("add_trade/", views.add_trade, name ="add_trade"),
    path("reg/", views.reg, name="reg"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]