# Import path for routing and views from views1.py
from django.urls import path
from myapp import views1

# Application namespace
app_name = 'myapp'

# URL patterns for the app
urlpatterns = [

    # Landing page showing books and publishers
    path('', views1.index, name='index'),

    # About page
    path('about/', views1.about, name='about'),

    # Book detail page with dynamic book_id
    path('<int:book_id>/', views1.detail, name='detail'),
]
