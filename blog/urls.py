from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('', views.LandingPage, name='landing_page'),
    path('category/<int:category_id>/', views.CategoryPosts, name='category_post'),
    path('category/', views.CategoryList, name='category_list'),
    path('post/<int:post_id>/', views.PostDetails, name='post_detail'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
]
