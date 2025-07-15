# Import necessary Django classes
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Publisher, Book, Member, Order  # Import models

# View for the index page: shows list of books and publishers
def index(request):
    response = HttpResponse()

    # PART 1.a (initial): Order books by title
    '''
    # Get all books ordered by title
    booklist = Book.objects.all().order_by('title')[:10]    # only first 10 books
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)
    '''

    # PART 1.e (final): Order books by primary key (id)
    # Get all books ordered by primary key (id)
    books = Book.objects.all().order_by('id')
    response.write('<h2>List of available books:</h2>')
    for book in books:
        response.write(f'<p>{book.id}: {book}</p>')

    # List of publishers ordered by city descending
    publishers = Publisher.objects.all().order_by('-city')
    response.write('<h2>List of publishers (by city):</h2>')
    for pub in publishers:
        response.write(f'<p>{pub.name} - {pub.city}</p>')

    return response

# Solution for 2.
# View for the 'about' page
def about(request):
    return HttpResponse("This is an eBook APP.")

# Solution for 3 and 4.
# View to show details of a specific book using its ID
def detail(request, book_id):
    # Get the book object or return 404 if not found
    book = get_object_or_404(Book, pk=book_id)

    # Return formatted response with book info
    return HttpResponse(
        f"<h3>{book.title.upper()}</h3>"                # Title in uppercase
        f"<p>Price: ${book.price}</p>"                  # Price with $
        f"<p>Publisher: {book.publisher.name}</p>"      # Publisher name
    )
