from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Book, Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect('store:home')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store:home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('store:home')


def home(request):
    books = Book.objects.all()
    return render(request, 'store/home.html', {'books': books})


@login_required
def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add books to your cart.")
        return redirect('store:login')
    
    book = Book.objects.get(id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user, book=book)
    cart.quantity += 1
    cart.save()
    messages.success(request, f"Added {book.title} to your cart.")
    return redirect('store:home')

@login_required
def update_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity <= 0:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.book.title} from your cart.")
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Updated {cart_item.book.title} in your cart.")
    return redirect('store:cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'store/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def make_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('store:book_list')

    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)
        item.book.stock -= item.quantity  # Update the book stock
        item.book.save()
        item.delete()  # Remove from cart

    order.status = 'Confirmed'
    order.save()
    messages.success(request, "Your order has been placed!")
    return redirect('store:order_detail', order_id=order.id)


def order_detail(request, order_id):
    # Get the order by its ID
    order = get_object_or_404(Order, id=order_id)

    # Make sure the order belongs to the logged-in user
    if order.user != request.user:
        return redirect('store:home')  # Redirect to home if the order doesn't belong to the user

    # Pass the order to the template
    return render(request, 'store/order_detail.html', {'order': order})