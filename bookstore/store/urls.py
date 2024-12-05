from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('make_order/', views.make_order, name='make_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
