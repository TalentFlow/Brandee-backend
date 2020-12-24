from django.contrib import admin
from django import forms
from .models import ( Product , Wishlist , ProductPhotos, Sizes,
 HomePhotos, OrderItems, Order,Address,Payment)
from django.db import models
from cloudinary.models import CloudinaryField



# @admin.register(Information)
# class InformationAdmin(admin.ModelAdmin):

#     # formfield_overides={
#     #     models.TextField:{'widget': TinyMCE() },
#     # }
    
#     list_display=('title','description')
#     list_filter=('title',)
#     search_fields=['title', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','slug', 'Date']
    list_filter = ('title','slug','Date')
    search_fields = ['title','slug']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    
    list_display = ['product','user', 'Date']
    list_filter = ('product','Date')
    search_fields = ['user__username','product__title']


@admin.register(ProductPhotos)
class ProductPhotosAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]

@admin.register(HomePhotos)
class HomePhotosAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["products"]
    
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Address)
# admin.site.register(HomePhotos)
admin.site.register(Sizes)