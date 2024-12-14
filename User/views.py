from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, PostForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from django.core.paginator import Paginator
from blog.models import Post, Like, Category, Comment
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, EditUserProfileForm
from django.http import JsonResponse


# functions related to User
def UserHome(request):
    posts = Post.objects.all()
    categories = Category.objects.all()

    # Implement pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the posts for the current page

    return render(request, 'user/user_home.html', {'posts': page_obj, 'categories': categories})

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

@login_required
def EditUserProfile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.first_name}'s profile updated successfully!")
            return redirect('user_home')
    else:
        form = EditUserProfileForm(instance=user)

    return render(request, 'user/edit_user_profile.html', {'form': form, 'user': user})

@login_required
def UserAccount(request):
    user = request.user
    user_posts = Post.objects.filter(author=user)

    # Calculate total likes on user's posts
    total_likes = sum(post.likes.count() for post in user_posts)

    # Calculate total comments on user's posts
    total_comments = Comment.objects.filter(post__author=user).count()

    context = {
        'user': user,
        'total_posts': user_posts.count(),
        'total_likes': total_likes,
        'total_comments': total_comments,
        'posts': user_posts,
    }

    return render(request, 'user/user_account.html', context)

def UserCategoryList(request):
    categories = Category.objects.all()
    return render(request, 'user/user_category_list.html', {'categories': categories})

# def AddCategory(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Category added successfully!")
#             return redirect('admin_category_list')
#     else:
#         form = CategoryForm()
#     return render(request, 'admin/user_add_category.html', { 'form': form})

def UserCategoryPosts(request, category_id):
    # Get the category based on the ID
    category = get_object_or_404(Category, id=category_id)

    # Filter posts by the category
    posts = Post.objects.filter(category=category)

    # Render the posts to the template
    return render(request, 'user/user_category_posts.html', {'category': category, 'posts': posts})


@login_required
def UserPosts(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'user/users_own_posts.html', {'user_posts': user_posts})

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

    return render(request, 'user/user_post_detail.html', {
        'post': post,
        'comments': comments,
        'user_like': user_like,
        'like_count': like_count,
    })

@login_required
def AddPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Create the post object without saving it
            post.author = request.user      # Assign the logged-in user as the author
            print(f"Post Author: {post.author}")  # Debugging: Check the author
            post.save()                     # Save the post
            messages.success(request, "Post created successfully!")
            return redirect('user_own_post')  # Redirect to the user's posts list
    else:
        form = PostForm()

    return render(request, 'user/add_user_post.html', {'form': form})

@login_required
def EditPost(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('user_own_post')
    else:
        form = PostForm(instance=post)
    return render(request, 'user/edit_post.html', {'form': form, 'post': post})

@login_required
def DeletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('user_own_post')
    return render(request, 'user/delete_user_post.html', {'post': post})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    # Check if the user has already liked the post
    like_obj = Like.objects.filter(post=post, user=user).first()

    if like_obj:
        if like_obj.is_like:
            like_obj.is_like = False  # Unlike the post
            action = 'unliked'
        else:
            like_obj.is_like = True  # Like the post
            action = 'liked'
        like_obj.save()
    else:
        # If the user hasn't liked the post, create a new Like object
        Like.objects.create(post=post, user=user, is_like=True)
        action = 'liked'

    # Return updated like count and like status
    return JsonResponse({
        "like_count": post.likes.filter(is_like=True).count(),
        "user_like": action == 'liked',
        "action": action,
    })

@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # Parse the JSON content from the request body
        import json
        data = json.loads(request.body)

        # Extract the comment content
        content = data.get('content')
        if content:
            # Create and save the comment
            comment = Comment.objects.create(post=post, author=request.user, content=content)

            # Return the newly added comment's data as JSON
            return JsonResponse({
                "author": comment.author.first_name,
                "content": comment.content,
                "created_at": comment.created_at,
            })
        else:
            return JsonResponse({"error": "No content provided"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)





# functions related to Admin
def AdminHome(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    user = request.user
    print("user:", user)
    print("categories:", categories)
    print("first_name: ", user.first_name)
    print("image: ", user.profile_picture)
    return render(request, 'admin/admin_home.html', {'posts': posts, 'categories': categories})

def AdminCategoryList(request):
    categories = Category.objects.all()
    return render(request, 'admin/admin_category_list.html', {'categories': categories})


def AdminCategoryPosts(request, category_id):
    # Get the category based on the ID
    category = get_object_or_404(Category, id=category_id)

    # Filter posts by the category
    posts = Post.objects.filter(category=category)

    # Render the posts to the template
    return render(request, 'admin/admin_category_post.html', {'category': category, 'posts': posts})

def AddCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('admin_category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/add_category_list.html', { 'form': form})

@login_required
def EditCategory(request, category_id):
    # Fetch the category using the provided ID
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # Create a form instance with the POST data and the category instance
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            # Save the form if it's valid
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('admin_category_list')  # Redirect to category list after update
    else:
        # Pre-fill the form with the current category details
        form = CategoryForm(instance=category)

    return render(request, 'admin/edit_category.html', {'form': form, 'category': category})

@login_required
def DeleteCategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        # Delete the category
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('admin_category_list')  # Redirect to the category list after deletion

    return render(request, 'admin/confirm_delete_category.html', {'category': category})

@login_required
def AdminPosts(request):
    admin_posts = Post.objects.filter(author=request.user)

    # Implement pagination
    paginator = Paginator(admin_posts, 1)
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the posts for the current page
    return render(request, 'admin/admin_own_posts.html', {'admin_posts': page_obj})


@login_required
def AdminAddPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('admin_own_post')  # Redirect to the user's posts list
    else:
        form = PostForm()

    return render(request, 'admin/add_admin_post.html', {'form': form})


@login_required
def AdminPostDetails(request, post_id):
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

    return render(request, 'admin/admin_post_detail.html', {
        'post': post,
        'comments': comments,
        'user_like': user_like,
        'like_count': like_count,
    })

@login_required
def AdminEditPost(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('admin_post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'admin/admin_edit_post.html', {'form': form, 'post': post})


@login_required
def AdminDeletePost(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('admin_own_post')
    return render(request, 'admin/delete_admin_post.html', {'post': post})

@login_required
def MyAccount(request):
    user = request.user
    user_posts = Post.objects.filter(author=user)

    # Calculate total likes on user's posts
    total_likes = sum(post.likes.count() for post in user_posts)

    # Calculate total comments on user's posts
    total_comments = Comment.objects.filter(post__author=user).count()

    context = {
        'user': user,
        'total_posts': user_posts.count(),
        'total_likes': total_likes,
        'total_comments': total_comments,
        'posts': user_posts,
    }

    return render(request, 'admin/my_account.html', context)

@login_required
def EditAdminProfile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, request.FILES,  instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{user.first_name}'s profile updated successfully!")
            return redirect('admin_my_account')
    else:
        form = EditUserProfileForm(instance=user)

    return render(request, 'admin/edit_user_profile.html', {'form': form, 'user': user})
