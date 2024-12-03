from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from blog.models import Post, Like, Category, Comment
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm
def UserHome(request):
    return render(request, 'user_home.html')

def AdminHome(request):
    return render(request, 'admin_home.html')

# Create your views here.
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate user using email instead of username
            user = authenticate(request, username=email, password=password)
            print("user: ", user.is_staff)
            print("user: ", user.is_superuser)
            if user is not None:
                if user.is_superuser and user.is_staff:
                    login(request, user)
                    return redirect('admin_home')  # Redirect to the homepage or any other page after login
                else:
                    login(request, user)
                    return redirect('user_home')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('landing_page')

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extracting data from the form
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            # Ensure the passwords match
            if password != password_confirm:
                messages.error(request, "Passwords do not match")
                return redirect('signup')

            # # Check if there are any existing users in the database
            # is_first_user = CustomUser.objects.count() == 0
            #

            # Create the new user using the custom manager
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # # If this is the first user, make them an admin
            # if is_first_user:
            #     user.is_staff = True
            #     user.is_superuser = True
            #     user.save()

            # Log the user in after successful registration
            login(request, user)
            # print("user: ", user.is_staff)
            # print("user: ", user.is_superuser)
            # # Redirect based on whether the user is admin or not
            # if user.is_superuser and user.is_staf:
            #     return redirect('admin_home')  # Change to your admin home view
            # else:
            return redirect('login')  # Change to your user home view

    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})

def UserCategoryList(request):
    # Handle form submission
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('user_category_list')
    else:
        form = CategoryForm()

    # Fetch all categories
    categories = Category.objects.all()
    return render(request, 'user_category_list.html', {'categories': categories, 'form': form})

def UserCategoryPosts(request, category_id):
    # Get the category based on the ID
    category = get_object_or_404(Category, id=category_id)

    # Filter posts by the category
    posts = Post.objects.filter(category=category)

    # Render the posts to the template
    return render(request, 'user_category_posts.html', {'category': category, 'posts': posts})

@login_required
def UserPostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)

    # Fetch all comments for the post
    comments = post.comments.all()

    # Fetch like status
    user_like = post.likes.filter(user=request.user, is_like=True).exists()
    like_count = post.likes.filter(is_like=True).count()

    return render(request, 'user_post_detail.html', {
        'post': post,
        'comments': comments,
        'user_like': user_like,
        'like_count': like_count,
    })
