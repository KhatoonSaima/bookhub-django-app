from django import forms
from myapp.models import CATEGORY_CHOICES, Order

# Form to collect user preference for borrowing or purchasing books
class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)

# Form that allows users to enter their name(optional), select a book category (optional),
# and specify a maximum price to search for books
class SearchForm(forms.Form):
    name = forms.CharField(label='Your Name', required=False)
    category = forms.ChoiceField(
        label='Select a category:',
        choices=CATEGORY_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)

# ModelForm based on the Order model, used to create new book orders
# Allows selection of books, member, and order type (purchase or borrow)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'order_type': forms.RadioSelect,
        }
        labels = {
            'member': 'Member name',
        }