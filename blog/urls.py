from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Other URL patterns
    path('', views.LandingPage, name='landing_page'),
    path('about/', views.AboutPage, name='about'),
    path('contact/', views.ContactPage, name='contact_page'),

    path('category/<int:category_id>/', views.CategoryPosts, name='category_post'),
    path('category/', views.CategoryList, name='category_list'),
    path('post/', views.AllPosts, name='all_posts'),
    path('post/<int:post_id>/', views.PostDetails, name='post_detail'),

    # path('accounts/login/', views.custom_login, name='login'),  # Custom login URL
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    # path('post/<int:post_id>/like/', views.toggle_like, name='post_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='post_comment'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)