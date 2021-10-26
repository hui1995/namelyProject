from django.contrib import admin
from books.models import Book,Category,Comment
# # Register your models here.
#
class BookAdmin(admin.ModelAdmin):
    list_display = ('title',"category",'star')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','book',"content")

admin.site.register(Book,BookAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)
