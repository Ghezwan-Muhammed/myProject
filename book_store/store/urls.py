from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('order/<int:book_id>/', views.place_order, name='place_order'),
    path('register/', views.register, name='register'),  # Registration URL
    path('logout/', LogoutView.as_view(), name='logout'),
    
]