from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to = 'photos/', blank=True, null=True)

    def __str__(self):
        return self.first_name


class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author_first_name = models.CharField(max_length=100)
    author_last_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    year = models.IntegerField()
    genre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_banner = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'photos/', blank=True, null=True )
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    



class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Foydalanuvchini qo'shish
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.book}'