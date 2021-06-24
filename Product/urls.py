from django.urls import path,re_path
from . import views
urlpatterns = [
    path('single_product/<int:id>/', views.single_product, name="single_product"),
    path('category_product/<int:id>/<slug:slug>/', views.category_product, name="category_product"),
    path('searchproducts/', views.searchproducts, name="searchproducts"),
    path('add_comment/<int:id>/', views.Comment_Add, name="Comment_Add"),


]
