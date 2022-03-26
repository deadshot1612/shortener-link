from django.urls import path

from account import views


urlpatterns = [
    path('login/', views.log_user_in, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<int:uid>/<str:token>', views.activate_user, name='activate'),
    path('login/<int:pk>/confirm', views.login_confirm, name='login-confirm')
]