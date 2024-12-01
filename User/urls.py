from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('login/', views.Login, name='login'),
    path('signup/', views.Register, name='signup'),
    path('logout/', views.Logout, name='logout'),

    path('user_home/', views.UserHome, name='user_home'),
    path('admin_home/', views.AdminHome, name='admin_home'),
]