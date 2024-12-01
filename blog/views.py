from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Like, Category
from django.contrib.auth import authenticate, login
from django.contrib import messages

def LandingPage(request):
    return render(request, 'landing_page.html')


def CategoryList(request):
    categories = Category.objects.all()
    print(" categories:",categories)
    return render(request, 'category_list.html', {'categories':categories})


def CategoryPosts(request, category_id):
    # Get the category based on the ID
    category = get_object_or_404(Category, id=category_id)

    # Filter posts by the category
    posts = Post.objects.filter(category=category)

    # Render the posts to the template
    return render(request, 'category_posts.html', {'category': category, 'posts': posts})


def PostDetails(request, post_id):
    # Retrieve the post by its ID
    post = get_object_or_404(Post, id=post_id)

    # Render the post details page
    return render(request, 'post_detail.html', {'post': post})





def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user = request.user  # Assume the user is authenticated.

        # Check if the user already has a like/unlike for this post
        like_obj, created = Like.objects.get_or_create(post=post, user=user)

        # Toggle between like and unlike
        if like_obj.is_like:
            like_obj.is_like = False  # Unlike
            action = 'unliked'
        else:
            like_obj.is_like = True  # Like
            action = 'liked'

        like_obj.save()

        # Example response: Return an HTTP response indicating the action performed
        return HttpResponse(f"Post {action} successfully!")

    return HttpResponse("Invalid request method.", status=405)  # Method Not Allowed
