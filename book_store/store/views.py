from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'store/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'store/book_detail.html', {'book': book})

@login_required
def place_order(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    # Get the quantity from the form submission
    quantity = int(request.POST.get('quantity', 1))

    # Check if there is enough stock
    if book.stock >= quantity:
        # Create and save the order
        order = Order(book=book, quantity=quantity)
        order.save()

        # Update the book's stock
        book.stock -= quantity
        book.save()

        # Show a confirmation message
        messages.success(request, f"Your order for {quantity} copies of '{book.title}' has been placed successfully!")
        return render(request, 'store/order_confirmation.html', {'order': order})

    else:
        # If there isn't enough stock, show an error message
        messages.error(request, f"Sorry, we only have {book.stock} copies of '{book.title}' in stock.")
        return redirect('book_detail', book_id=book.id)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})