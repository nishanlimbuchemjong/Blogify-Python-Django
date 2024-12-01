from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Like, Category
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib import messages

def LandingPage(request):
    return render(request, 'landing_page.html')

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate user using email instead of username
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the homepage or any other page after login
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extracting data from the form
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            # Ensure the passwords match
            if password != password2:
                messages.error(request, "Passwords do not match")
                return redirect('signup')

            # Create the new user using the custom manager
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Log the user in after successful registration
            login(request, user)

            # Redirect to a success page (for example, homepage)
            return redirect('home')  # Change this to whatever your homepage view is called

    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})

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
