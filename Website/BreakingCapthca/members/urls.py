from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('reset_user_password', views.reset_user_password, name='resetPass')
    path('reset_user_password_done', views.reset_user_password_done, name='resetPassDone')
]
