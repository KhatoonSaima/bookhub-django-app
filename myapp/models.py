from django.db import models  # Import Django's base model class
from django.contrib.auth.models import User  # (Optional) For user associations if needed
from django.utils import timezone


# Model representing a book publisher
class Publisher(models.Model):
    name = models.CharField(max_length=200)  # Name of the publisher
    website = models.URLField()              # Publisher's official website URL
    city = models.CharField(max_length=20, blank=True)  # Optional city field
    country = models.CharField(max_length=50, default='USA') # Headquarter of the publisher

    def __str__(self):
         return self.name  # Return publisher name in admin interface


# using it is views.py file
CATEGORY_CHOICES = [  # Dropdown choices for book categories
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
# Model representing a book
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')  # Category selection
    num_pages = models.PositiveIntegerField(default=100)  # Number of pages (must be positive)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Book price
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    # Foreign key linking to Publisher, with cascading delete behavior
    description = models.TextField(blank=True, null=True)   # Description of the book

    def __str__(self):
        return self.title  # Display book title in admin and shell

# Model representing a member
class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank=True)  # Made optional
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.username   # Return the username as the string representation of the Member

# Model representing a order
# Model representing a book order by a member.
# Supports both purchase and borrow types, and tracks the order date.
class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        (0, 'Purchase'),
        (1, 'Borrow'),
    ]
    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)

    def total_items(self):
        return self.books.count()    # Return the total number of books in the order

    def __str__(self):
       return f"Order #{self.pk} by {self.member.username}"     # Return order ID and member username

