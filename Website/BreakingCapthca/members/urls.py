from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="members/password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="authenticate/password_reset_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>', 
         auth_views.PasswordResetConfirmView.as_view(template_name="members/password_reset_C.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="members/password_reset.html"), 
         name="password_reset_complete")
]
