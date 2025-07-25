from django.shortcuts import render, get_object_or_404
from .models import Book, CATEGORY_CHOICES
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# View to display the index page with a list of books
@login_required(login_url='/myapp/login/')
def index(request):
    # Get the first 10 books ordered by ID
    booklist = Book.objects.all().order_by('id')[:10]

    # Previously rendered index0.html (basic HTML without inheritance)
    #return render(request, 'myapp/index0.html', {'booklist': booklist})

    # Now render index.html which extends base.html using template inheritance
    return render(request, 'myapp/index.html', {'booklist': booklist})

# View to display the about page
def about(request):
    # No extra context variables are needed for the about page

    # Previously rendered about0.html (basic HTML without inheritance)
    #return render(request, 'myapp/about0.html')

    # Now render about.html which extends base.html using template inheritance
    return render(request, 'myapp/about.html')

# View to display book details based on book_id
def detail(request, book_id):
    # Do you need to pass any extra context variables to the template?   YES      NO
    # YES - Passing 'book' object as context to the template

    # Retrieve the book with the given ID or return 404 if not found
    book = get_object_or_404(Book, pk=book_id)
    #book = Book.objects.get(pk=book_id)

    # Previously rendered detail0.html (basic HTML without inheritance)
    #return render(request, 'myapp/detail0.html', {'book': book})

    # Now render detail.html which extends base.html using template inheritance
    return render(request, 'myapp/detail.html', {'book': book})


# View to display and process the feedback form
# Shows borrow/purchase choices and displays user selection on submission
def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = 'to borrow books.'
            elif feedback == 'P':
                choice = 'to purchase books.'
            else:
                choice = 'None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})


# View to display a search form and filter books based on user input
# Filters books by optional category and a maximum price threshold
# Displays results along with a greeting message
def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category_code = form.cleaned_data['category']   # e.g. F for Fiction
            max_price = form.cleaned_data['max_price']

            print(f"name: {name}, category: {category_code}, max_price: {max_price}")

            # Get display label
            category_label = dict(CATEGORY_CHOICES).get(category_code, 'All Categories')
            print(f"category_label: {category_label}")

            # Query books
            if category_code:
                booklist = Book.objects.filter(category=category_code, price__lte=max_price)
                #print(f"booklist: {booklist}")
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {
                'name': name,
                'category_label': category_label,
                'booklist': booklist
            })

        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})

# View to place a new order using the OrderForm
# Saves selected books and associates them with a member
# If order type is 'borrow', adds books to member's borrowed list
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)     # Creates an Order object (not saved yet)
            member = order.member
            type = order.order_type
            order.save()                        # Now save to DB
            form.save_m2m()                     # Save selected books to the M2M relationship

            if type == 1:  # 1 = Borrow
                for b in order.books.all():
                    member.borrowed_books.add(b)

            return render(request, 'myapp/order_response.html', {
                'books': books,
                'order': order
            })
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})

"""
Handle user login functionality.

If the request method is POST, extract the username and password from the form,
authenticate the user using Django's built-in authentication system,
and log them in if credentials are valid and the user is active.
Redirect to the index page on success or return an error message otherwise.

If the request method is GET, render the login form template.
"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

"""
Log out the currently authenticated user.

This view requires the user to be logged in (enforced by @login_required).
It logs out the user and redirects them to the index page.
"""
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))
