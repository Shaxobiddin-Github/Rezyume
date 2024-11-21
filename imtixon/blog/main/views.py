from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.core.handlers.wsgi import WSGIRequest 
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
# Create your views here.




from .models import Book,Category,Author,Comment
from .forms import LoginForm, RegisterForm,BookForm, AuthorForm



@method_decorator(login_required(login_url="login"), name='dispatch')
class HomeView(View):   
    
    def get(self, request):
        newsers = Book.objects.filter(is_active = True)
        newsers_photo_hikoya=Book.objects.filter(category= 1).last()
        newsers_hikoya=newsers.filter(category= 1)[:4]
        newsers_hikoya2=newsers.filter(category= 1)[5:8]
        newsers_photo_sher=newsers.filter(category= 2).last()
        latest_news = newsers.order_by("-created")[:4]  
        price_book = newsers.order_by("price").last()
        newsers_category_adabiyot = newsers.filter(category=2).order_by('-created')[:4]

        

        context={
             "newsers": newsers, 
             "title":"shaxobiddin",
             "newsers_photo_sher":newsers_photo_sher,
             "newsers_photo_hikoya":newsers_photo_hikoya,
             "latest_news":latest_news,
             "newsers_hikoya":newsers_hikoya,
             "newsers_hikoya2":newsers_hikoya2,
             "price_book":price_book,
             "newsers_category_adabiyot":newsers_category_adabiyot

        }
        
        return render(request, 'main/index.html', context)


class DetailView(View):
    def get(self, request,pk):
        book = get_object_or_404(Book, pk=pk)
        comments = Comment.objects.filter(book=book)
        news = Book.objects.get(pk=pk)
        categories = Category.objects.all()
        context = {
            "news":news,
            "categories":categories,
            "book":book,
            "comments":comments
        }
        
        return render(request, "main/detail.html",context)

    def post(self,request, pk):
        book = get_object_or_404(Book, pk=pk)
        comments = Comment.objects.filter(book=book)
        news = Book.objects.get(pk=pk)
        categories = Category.objects.all()
        context = {
            "news":news,
            "categories":categories,
            "book":book,
            "comments":comments
            
        }
        return render(request, "main/detail.html",context)


# @method_decorator(login_required(login_url="login"), name='dispatch')
class ProfileView(View):
    def get(self, request):
        return render(request, "profile.html",)

# ------------------------------------------AUTH----------------------------------------

class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        context={
            "login_form":login_form,
        }
        return render(request, "login.html",context)
    
    def post(self, request):
        if request.method == "POST":
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user=login_form.get_user()
                login(request,user)
                messages.success(request, f"Saytga xush kelibsiz {user.username}")
                return redirect('home')
            else:
                messages.error(request, "Login ushbu ma'lumotlardan chiqmagan edi")
        return render(request, "login.html", {"login_form": login_form})


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, f"Siz saytdan muvaffaqiyatli  chiqdingiz!!")
        return redirect('login')
    





class RegisterView(View):
    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tabriklaymiz......  \n  Siz muvaffaqiyatli ruyxatdan utdingiz\nLogin parolni terib saytimizga kiring!")
            return redirect('login')
        else:
            print(form.error_messages, "**********************************")

    def get(self, request):
        form = RegisterForm()
        context = {
            "form": form,
        }
        return render(request, "register.html", context)

# ------------------------------------------END-AUTH----------------------------------------



    







# --------------------------CREATE--------------------



class AddBookAuthorView(View):
    template_name_book = 'add_book.html'
    template_name_author = 'add_author.html'

    def get(self, request, form_type):
        if form_type == 'book':
            form = BookForm()
            return render(request, self.template_name_book, {'form': form})
        elif form_type == 'author':
            form = AuthorForm()
            return render(request, self.template_name_author, {'form': form})
        else:
            return redirect('home')  

    def post(self, request, form_type):
        if form_type == 'book':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = Book(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    author=form.cleaned_data['author'],
                    price=form.cleaned_data['price'],
                    year=form.cleaned_data['year'],
                    genre=form.cleaned_data['genre'],
                    image=form.cleaned_data['image'],
                )
                book.save()
                return redirect('book_list')  
        elif form_type == 'author':
            form = AuthorForm(request.POST, request.FILES)
            if form.is_valid():
                author = Author(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    birth_date=form.cleaned_data['birth_date'],
                    death_date=form.cleaned_data['death_date'],
                    biography=form.cleaned_data['biography'],
                    image=form.cleaned_data['image'],
                )
                author.save()
                return redirect('author_list')  

        return redirect('home')  





def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books}) 

def author_list_view(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})  











# -----------------------DELETE---------------------------




def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list') 
    return render(request, 'confirm_delete.html', {'object': book})

def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')  
    return render(request, 'confirm_delete.html', {'object': author})


# ----------------------------UPDATE-----------------------------------

class UpdateBookView(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(initial={
            'name': book.name,
            'description': book.description,
            'author': book.author,
            'price': book.price,
            'year': book.year,
            'genre': book.genre,
            'tag': ', '.join([tag.name for tag in book.tag.all()]),  # Taglarni olish
            'category': book.category,
            'image': book.image,
        })
        return render(request, 'add_book.html', {'form': form, 'book': book})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book.name = form.cleaned_data['name']
            book.description = form.cleaned_data['description']
            book.author = form.cleaned_data['author']
            book.price = form.cleaned_data['price']
            book.year = form.cleaned_data['year']
            book.genre = form.cleaned_data['genre']
           
            book.image = form.cleaned_data['image']
            book.save()
            return redirect('book_list')
        return render(request, 'add_book.html', {'form': form, 'book': book})

class UpdateAuthorView(View):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        form = AuthorForm(initial={
            'first_name': author.first_name,
            'last_name': author.last_name,
            'birth_date': author.birth_date,
            'death_date': author.death_date,
            'biography': author.biography,
            'image': author.image,
        })
        return render(request, 'add_author.html', {'form': form, 'author': author})

    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.birth_date = form.cleaned_data['birth_date']
            author.death_date = form.cleaned_data['death_date']
            author.biography = form.cleaned_data['biography']
            author.image = form.cleaned_data['image']
            author.save()
            return redirect('author_list')
        return render(request, 'add_author.html', {'form': form, 'author': author})



# ---------------------Comment-------------------


def save_comments(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        text = request.POST.get("text")  

        if not text:
            messages.error(request, "fikr qoldirishingiz kerak")
            return redirect('detail', pk=book_id) 
        
        Comment.objects.create(
            user=request.user,  
            book=book,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            text=text
        )
        messages.success(request, "Fikringiz uchun raxmat!!")
        return redirect('detail', pk=book_id)
    return redirect('detail', pk=book_id)
