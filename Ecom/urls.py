from django.urls import path,re_path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('contact/', views.contact, name="contact"),
]
