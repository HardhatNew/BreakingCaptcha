from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),

    path('reset_password/',  # form to submit email
        auth_views.PasswordResetView.as_view(template_name="authenticate/password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/', # form which says email sent
         auth_views.PasswordResetDoneView.as_view(template_name="authenticate/password_reset_sent.html"), 
         name="password_reset_done"),

     # uidb64 = user id encoded in base64
    path('reset/<uidb64>/<token>',  # form which allows for password to be reset
         auth_views.PasswordResetConfirmView.as_view(template_name="authenticate/password_reset_C.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/',  #form which confirms password has been reset
         auth_views.PasswordResetCompleteView.as_view(template_name="authenticate/password_reset.html"), 
         name="password_reset_complete")
]
