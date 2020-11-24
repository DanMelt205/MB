from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('userpage/', views.UserProfileView.as_view(), name='userprofiles'),
    path('userpage/<int:pk>', views.UserProfileUpdateView.as_view(),
         name='userprofilesupdate'),

    path('reset_password/', views.PasswordResetCustomUser.as_view(),
         name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='register/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetCustomUserConfirm.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='register/password/password_reset_complete.html'), name='password_reset_complete'),
]
