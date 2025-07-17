from django.urls import path
from myapp import views

app_name = 'myapp'

# URL patterns for the app
urlpatterns = [
    path('', views.index, name='index'),        # URL for index page

    # About page
    path('about/', views.about, name='about'),      # URL for about page

    # Detail page
    # myapp/<book_id>
    path('<int:book_id>/', views.detail, name='detail'),        # URL for book detail page

    # Feedback form
    path('feedback/', views.getFeedback, name='feedback1'),

    # Search form
    path('findbooks/', views.findbooks, name='findbooks'),

    # Order form
    path('place_order/', views.place_order, name='place_order'),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),
]
