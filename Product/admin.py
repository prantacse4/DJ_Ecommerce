from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Company)


class PImageInline(admin.TabularInline):
    model = Images
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'company', 'created_at', 'updated_at', 'image_tag']
    list_filter  = ['title', 'created_at']
    list_per_page = 10
    search_fields = ['title', 'new_price', 'details']
    inlines = [PImageInline]
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Product, ProductAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'status', 'created_at', 'updated_at', 'user']
    list_filter  = ['status', 'created_at']
    list_per_page = 10

admin.site.register(Comment, CommentAdmin)


