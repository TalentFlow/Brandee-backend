from rest_framework import serializers
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import (Product, Sizes, Wishlist,
 ProductPhotos, ProductPhotos,HomePhotos,Order,OrderItems,Address)
from django.contrib.auth import get_user_model # If used custom user model
import json
from django.http import JsonResponse

UserModel = get_user_model()







class ProductGeneralSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model= Product
        fields=['id','title','slug','img','color','price_new','price_old']

    def get_img(self, obj):

        images = ProductPhotos.objects.filter(product=obj.id)
        images2= ProductPhotosSerializer(images,many=True)

        return images2.data

class OrderItemSerializer(serializers.ModelSerializer):
    products=ProductGeneralSerializer()
    class Meta:
        model= OrderItems
        fields=['id','quantity','user','size','products','ordered','total','price']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model= Order
        fields=['id','user','items','total','ordered']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Sizes
        fields='__all__'





class ProductPhotosSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model= ProductPhotos
        fields=['id','product','img','is_featured','Date','updated']

    def get_img(self, document):
        # request = self.context.get('request')
        # print(request)
        file_url = document.img.url
        # print(file_url)
        return file_url

    

    
    

class HomePhotosSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta:
        model= HomePhotos
        fields=['id','img','img_catagory','Date','updated']

    def get_img(self, document):
        request = self.context.get('request')
        file_url = document.img.url
        print(file_url)
        return request.build_absolute_uri(file_url)
        



class ProductSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    wishlisted = serializers.SerializerMethodField()
    sizes=SizeSerializer(read_only=True, many=True)
    in_cart=serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','title', 'img','color','catagory','shoes_catagory','bags_catagory','boutique_catagory','jewellery_catagory','glasses_catagory','fitness_apparel_catagory','maternity_store_catagory',
        'under_garments_catagory','is_featured','wishlisted','in_cart','is_new','on_sale','slug',
        'Date','information','sizes','price_new','price_old']

    def get_img(self, obj):

        images = ProductPhotos.objects.filter(product=obj.id)
        images2= ProductPhotosSerializer(images,many=True)

        return images2.data

    def get_wishlisted(self, obj):

        user1 = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user1 = request.user
        # print(user1)
        user = self.context['user']
        # print(user)
        products = Wishlist.objects.filter(product=obj.id)
        user1=products.filter(user=user)

        if user1:
            return True
        return False
    
    def get_in_cart(self,obj):
        user = self.context['user']
        order_qs=Order.objects.filter(user=user)
        if order_qs.exists():
            order=order_qs[0]
            if order.items.filter(products=obj.id,ordered=False).exists():
                return True
            else:
                return False
        return False

class ProductGetSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    wishlisted = serializers.SerializerMethodField()
    sizes=SizeSerializer(read_only=True, many=True)
    in_cart=serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','title', 'img','color','catagory','shoes_catagory','bags_catagory','boutique_catagory','jewellery_catagory','glasses_catagory','fitness_apparel_catagory','maternity_store_catagory',
        'under_garments_catagory','is_featured','wishlisted','in_cart','is_new','on_sale','slug',
        'Date','information','sizes','price_new','price_old']

    def get_img(self, obj):
        
        images = ProductPhotos.objects.filter(product=obj.id)
        images2= ProductPhotosSerializer(images,many=True)

        return images2.data

    def get_wishlisted(self, obj):

        user1 = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user1 = request.user
        # print(user1)
        user = self.context['user']
        # print(user)
        products = Wishlist.objects.filter(product=obj.id)
        user1=products.filter(user=user)

        if user1:
            return True
        return False
    
    def get_in_cart(self,obj):
        user = self.context['user']
        order_qs=Order.objects.filter(user=user,ordered=False)
        if order_qs.exists():
            order=order_qs[0]
            if order.items.filter(products=obj.id,ordered=False).exists():
                return True
            else:
                return False
        return False
        
class WishlistGetSerializer(serializers.ModelSerializer):
    product=ProductGeneralSerializer()
    class Meta:
        model=Wishlist
        fields = ['id', 'user', 'product']

class ProductWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product']

    def create(self, request):
        data = request.data
        print(data)
        wish = Wishlist()
        wish.user = UserModel.objects.get(id=data["user"])
        wish.product = Product.objects.get(id=data["product"])
        wish.save()
        return wish

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id","user","first_name","last_name",
    "company","address1","address2","city","country",
    "postal","phone","default","name"]