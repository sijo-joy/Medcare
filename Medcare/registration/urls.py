from django.urls import path
from django.contrib.auth import views as auth_views



from . import views
urlpatterns = [
    path('logout', views.logoutUser, name='account_signout'),
    path('registerPage', views.registerPage, name='account_signup'),
    path('login', views.loginPage, name='account_login'),
    path('login/<slug:next>/', views.loginPage,),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),
]
