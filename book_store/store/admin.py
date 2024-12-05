from django.contrib import admin
from .models import Book, Author

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100px" />'
        return 'No image'
    image_preview.allow_tags = True  # Allow HTML to display the image preview

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
