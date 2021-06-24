from django.urls import path,re_path
from . import views
urlpatterns = [
    path("add_to_cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("add_to_wishlist/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("cart_details/", views.cart_details, name="cart_details"),
    path("mywishlist/", views.mywishlist, name="mywishlist"),
    path("cart_delete/<int:id>/", views.cart_delete, name="cart_delete"),
    path('checkOut/', views.CheckOut, name="checkout"),
    path('order_showing/', views.Order_showing, name="Order_showing"),
    path('order_product_showing/', views.Order_Product_showing, name="Order_Product_showing"),
    path("user_order_details/<int:id>/", views.user_order_details, name="user_order_details"),
    path("ordered_product_details/<int:id>/<int:oid>/", views.user_order_product_details, name="user_order_product_details"),
    path('update_cart_qty/<int:id>/', views.update_cart_qty, name="update_cart_qty"),
]
