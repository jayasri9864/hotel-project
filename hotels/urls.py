from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("menu/<int:pk>/", views.food_detail, name="food_detail"),
    path("order/<int:pk>/place/", views.place_order, name="place_order"),
    path("contact/", views.contact, name="contact"),
]