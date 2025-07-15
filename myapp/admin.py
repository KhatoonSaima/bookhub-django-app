from django.contrib import admin  # Import admin module
from .models import Publisher, Book, Member, Order # Import models from the current app

# Register Publisher model with Django admin
admin.site.register(Publisher)

# Register Book model with Django admin
admin.site.register(Book)

# Register Member model with Django admin
admin.site.register(Member)

# Create a custom admin class for Order to show total number of books
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'order_type', 'order_date', 'total_items_display')

    def total_items_display(self, obj):
        return obj.total_items()     # Use model method to count books in the order
    total_items_display.short_description = 'Total Books'   # Column header name

# Register Order model with Django admin
admin.site.register(Order, OrderAdmin)

# After registration, these models will be available at http://127.0.0.1:8000/admin/


