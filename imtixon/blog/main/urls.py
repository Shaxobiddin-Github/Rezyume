from django.contrib import admin
from django.urls import path
from .views import (HomeView, DetailView,LoginView,LogoutView,
                     RegisterView, ProfileView, AddBookAuthorView,
                     book_list_view,author_list_view,
                     delete_book, delete_author,
                     UpdateAuthorView,UpdateBookView,
                     save_comments)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('detail/<int:pk>', DetailView.as_view(), name="detail"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('add-book/', AddBookAuthorView.as_view(), {'form_type': 'book'}, name='add_book'),
    path('book-list/', book_list_view, name='book_list'), 
    path('add-author/', AddBookAuthorView.as_view(), {'form_type': 'author'}, name='add_author'),
    path('author-list/', book_list_view, name='author_list'), 
    path('delete-book/<int:pk>/', delete_book, name='delete_book'),  # Kitobni o'chirish
    path('delete-author/<int:pk>/', delete_author, name='delete_author'),  # Muallifni o'chirish
    path('update-book/<int:pk>/', UpdateBookView.as_view(), name='update_book'),  # Kitobni yangilash
    path('update-author/<int:pk>/', UpdateAuthorView.as_view(), name='update_author'), 
    path('save_comments/<int:book_id>', save_comments, name='add_comments'),
]
