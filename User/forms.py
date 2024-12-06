from django import forms
from blog.models import Category, Post

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return password_confirm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a brief description (optional)',
                'rows': 4,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Description',
            'image': 'Upload Image',
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']  # Include fields you want to manage
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the post title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your content here',
                'rows': 6,
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Content',
            'category': 'Category',
        }