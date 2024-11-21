from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
# Register your models here.

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk','name')
    list_display_links = ('pk','name',)

# admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('pk','first_name','last_name')
    list_display_links = ('pk','first_name',)

# admin.site.register(Book)

admin.site.register(Tag)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('user', 'book', 'text', 'created_at','email','name')


class BookAdminForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget = CKEditorWidget() 

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk','name','is_active','is_banner','author_first_name')
    list_display_links = ('pk','name',)
    list_editable = ('is_active','is_banner')
    inlines = [
        CommentInline
    ]
    form = BookAdminForm