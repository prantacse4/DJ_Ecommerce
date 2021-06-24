from django.urls import path,re_path
from . import views
urlpatterns = [
    path('logout/', views.logout_user, name="logout_user"),
    path('login/', views.login_user, name="login_user"),
    path('signup/', views.signup_user, name="signup_user"),
    path('user_profile/', views.user_profile, name="user_profile"),
    path('user_update/', views.user_update, name="user_update"),
    path('change_password/', views.change_password, name="change_password"),
    path('user_comment/', views.user_comment, name="user_comment"),
    path('user_comment_delete/<int:id>/', views.comment_delete, name="comment_delete")
    
]
