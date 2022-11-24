from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # デフォルトの認証URLを取り込む
    path('',include('django.contrib.auth.urls')),
    
    path('register/',views.register,name='register'),
    
    path('logout_user/',views.logout_user,name='logout_user'),
]
