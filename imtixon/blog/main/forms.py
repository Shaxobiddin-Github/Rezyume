from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms

from .models import Book, Author, Category, Tag


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "id":"form3Example1cg",
        "class":"form-control form-control-lg"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "id":"form3Example3cg",
        "class":"form-control form-control-lg"
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"form3Example4cg",
        "class":"form-control form-control-lg"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"form3Example4cdg",
        "class":"form-control form-control-lg"
    }))

    class Meta:
        model = User
        fields = ('username', 'email')



class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "id":"form2Example1",
        "class":"form-control"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id":"form2Example2",
        "class":"form-control"
    }))

# -------------------------------update-----------------

from django import forms
from .models import Book, Author

class BookForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    price = forms.DecimalField(decimal_places=2, max_digits=8)
    year = forms.IntegerField()
    genre = forms.CharField(max_length=50)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all())  # Tag modelidan tanlash
    category = forms.ModelChoiceField(queryset=Category.objects.all())  # Sizga kerakli Categoryni olish uchun
    image = forms.ImageField(required=False)

class AuthorForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    birth_date = forms.DateField()
    death_date = forms.DateField(required=False)
    biography = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=50)


class TagForm(forms.Form):
    name = forms.CharField(max_length=50)


