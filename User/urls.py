from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('login/', views.Login, name='login'),
    path('signup/', views.Register, name='signup'),
    path('logout/', views.Logout, name='logout'),

    path('user_home/', views.UserHome, name='user_home'),
    path('category/<int:category_id>/', views.UserCategoryPosts, name='user_category_post'),
    path('category/', views.UserCategoryList, name='user_category_list'),
    # path('post/<int:post_id>/', views.UserPostDetails, name='user_post_detail'),
    path('post/<int:post_id>/', views.UserPostDetails, name='user_post_detail'),

    path('admin_home/', views.AdminHome, name='admin_home'),
]