from django.db import models

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_images/', default='book_images/default.jpg')  # Add this line

    def __str__(self):
        return self.title


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"Order of {self.book.title} - {self.quantity} pcs"
