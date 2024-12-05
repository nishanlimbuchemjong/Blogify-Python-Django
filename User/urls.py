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
    path('category/add', views.AddCategory, name='add_user_category'),

    path('posts/', views.UserPosts, name='user_own_post'),
    path('posts/add/', views.AddPost, name='add_user_post'),
    path('posts/<int:post_id>/edit/', views.EditPost, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.DeletePost, name='delete_post'),

    # path('post/<int:post_id>/', views.UserPostDetails, name='user_post_detail'),
    path('post/<int:post_id>/', views.UserPostDetails, name='user_post_detail'),

    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', views.post_comment, name='post_comment'),

    path('admin_home/', views.AdminHome, name='admin_home'),
]