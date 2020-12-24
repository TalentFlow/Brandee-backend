from products.models import (Product,ProductPhotos, Wishlist, HomePhotos,OrderItems,
Order,Address,Payment)
from rest_framework import generics,viewsets, serializers
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,filters
from django_filters import rest_framework as filters1
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from django.conf import settings
from accounts.models import User
from django.db.models import Q
import json

from .serializers import (ProductSerializer, ProductGetSerializer,
 ProductPhotosSerializer, ProductWishlistSerializer,HomePhotosSerializer
 ,OrderItemSerializer,OrderSerializer,WishlistGetSerializer,
 AddressSerializer)

import stripe
import random
import string
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))



class ProductListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['title',
            'slug',
            'catagory',
            'shoes_catagory',
            'bags_catagory',
            'boutique_catagory',
            'jewellery_catagory',
            'fitness_apparel_catagory',
            'maternity_store_catagory',
            'under_garments_catagory',
            'glasses_catagory',]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # print(self.request.query_params.get('product'))
        context.update(
            {
                "user": self.request.query_params.get('user'),
            }
        )
        return context

class ProductPhotosListView(generics.ListAPIView):
    queryset=ProductPhotos.objects.all()
    serializer_class=ProductPhotosSerializer()
    authentication_classes = []
    permission_classes = []
    

class ProductGetView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    filter_backends = (filters1.DjangoFilterBackend,)
    filter_fields = ["title","catagory","shoes_catagory","bags_catagory","boutique_catagory","jewellery_catagory",
    "fitness_apparel_catagory","maternity_store_catagory",'glasses_catagory',"under_garments_catagory"]
    permission_classes = []
    authentication_classes = []

    def get_serializer_context(self):
        context = super().get_serializer_context()
        print(self.request.query_params.get('product'))
        context.update(
            {
                "user": self.request.query_params.get('user'),
            }
        )
        return context


class ProductSingleGetView(generics.ListAPIView):
    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        slug = self.request.query_params.get('slug')
        # print(slug)
        queryset = Product.objects.filter(slug=slug)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # print(self.request.query_params.get('product'))
        context.update(
            {
                "user": self.request.query_params.get('user'),
            }
        )
        return context


class WishlistGetView(generics.ListAPIView):
    serializer_class = WishlistGetSerializer
    queryset = Wishlist.objects.all()
    filter_backends = (filters1.DjangoFilterBackend,)
    filter_fields = ("user", "product",)
    permission_classes = []
    authentication_classes = []

class ProductWishlistViewset(viewsets.ModelViewSet):
    serializer_class = ProductWishlistSerializer
    queryset = Wishlist.objects.all()
    filter_backends = (filters1.DjangoFilterBackend,)
    filter_fields = ("user", "product",)
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        print("Wish getView get called")
        wish = Wishlist.objects.all()
        serializer = ProductWishlistSerializer(wish)
        return Response(serializer.data)

    def create(self, request):
        print("Wish createView called")
        serializer = ProductWishlistSerializer(data=request.data)
        if serializer.is_valid():
            wish = serializer.create(request)
            if wish:
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class HomePhotosListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset=HomePhotos.objects.all()
    serializer_class=HomePhotosSerializer

class AddToCartView(APIView):
    permission_classes=[]
    def post(self, request,*args,**kwargs):
        slug=request.data.get('slug',None)
        user=request.data.get('user',None)
        quantity=request.data.get('quantity',None)
        user1=User.objects.get(id=user)
        print(user1)
        print(slug)
        if slug is None:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        if user is None:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        product=Product.objects.get(slug=slug)
        if product is None:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        print(product)
        if quantity is None:
            order_item, created=OrderItems.objects.get_or_create(products=product,user=user1,ordered=False)
        else:
            order_item, created=OrderItems.objects.get_or_create(products=product,user=user1,ordered=False,quantity=quantity)
        print(order_item)
        order_qs=Order.objects.filter(user=request.data.get('user'),ordered=False)
        print(order_qs)
        if order_qs.exists():
            # print("exist")
            order=order_qs[0]
            print(order)
            if order.items.filter(products__slug=product.slug).exists():
                if quantity is None:
                    print(quantity)
                    order_item.quantity+=1
                    order_item.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    order_item.quantity=quantity
                    order_item.save()
                    return Response(status=status.HTTP_200_OK)
            else:
                order.items.add(order_item)
                return Response(status=status.HTTP_200_OK)
        else:

            order=Order.objects.create(
                user=user1,
                ordered=False
            )
            order.items.add(order_item)
            print(order)
            return Response({"message":"Invalid Request"},status=status.HTTP_200_OK)

class CartItemQuantityUpdateView(APIView):
    permission_classes=[]
    def post(self, request, *args, **kwargs):

        slug=request.data.get('slug',None)
        user=request.data.get('user',None)
        if slug is None:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        # print(slug)
        if user is None:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        # print(user)
        user1=get_object_or_404(User, id=user)
        if user1 is None:
            return Response({"message":"User not exists"}, status=status.HTTP_400_BAD_REQUEST)
        # print(user1)
        product=get_object_or_404(Product, slug=slug)
        if product is None:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        # print(item)
        order_qs=Order.objects.filter(user=user1,ordered=False)
        # print(order_qs)
        if order_qs.exists():
            order=order_qs[0]
            if order.items.filter(products=product.id,ordered=False).exists():
                order_item=OrderItems.objects.filter(
                    products=product.id,
                    user=user,
                    ordered=False
                )[0]
                print(order_item)
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    order_item.delete()
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response({"message":"Item not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":"You do not have an active order"}, status=status.HTTP_400_BAD_REQUEST)
        


class OrderItemsListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes=[]
    queryset=OrderItems.objects.all()
    filter_backends = (filters1.DjangoFilterBackend,)
    filter_fields = ("user","ordered", "products","quantity","id")

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes=[]
    queryset=Order.objects.all()
    filter_backends = (filters1.DjangoFilterBackend,)
    filter_fields = ("user","ordered","id")


class DeleteItemFromCart(generics.DestroyAPIView):
    permission_classes=[]
    queryset=OrderItems.objects.all()

class NavbarMobileView(APIView):
    permission_classes=[]
    def post(self, request, *args, **kwargs):
        count_cart=0
        count_wish=0
        user=request.data.get('user')
        
        cart=Order.objects.filter(user=user).first()
        if cart:
            count_cart=OrderItems.objects.filter(user=user,ordered=False).count()
        else:
            count_cart=0
        count_wish=Wishlist.objects.filter(user=user).count()
        data={
            "cart":count_cart,
            "wishlist":count_wish
        }
        return Response(data)



class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes=[]
    queryset=Address.objects.all()
    filter_backends = (filters1.DjangoFilterBackend,)
    filter_fields = ("user","first_name","last_name",
    "company","address1","address2","city","country",
    "postal","phone","default")

class AddressCreateView(APIView):
    permission_classes=[]

    def post(self, request, *args, **kwargs):
        user=request.data.get('user',None)
        first_name=request.data.get('first_name',None)
        last_name=request.data.get('last_name',None)
        company=request.data.get('company',None)
        address1=request.data.get('address1',None)
        address2=request.data.get('address2',None)
        city=request.data.get('city',None)
        country=request.data.get('country',None)
        postal=request.data.get('postal',None)
        phone=request.data.get('phone',None)
        default=request.data.get('default',None)
        if user is None:
            return Response({"message":"There should b a user."}, status=status.HTTP_400_BAD_REQUEST)
        if first_name is None:
            return Response({"message":"There should b a first name."}, status=status.HTTP_400_BAD_REQUEST)
        if last_name is None:
            return Response({"message":"There should b a last name."}, status=status.HTTP_400_BAD_REQUEST)
        if company is None:
            return Response({"message":"There should b a company."}, status=status.HTTP_400_BAD_REQUEST)
        if address1 is None:
            return Response({"message":"There should b a address1"}, status=status.HTTP_400_BAD_REQUEST)
        if city is None:
            return Response({"message":"There should b a city"}, status=status.HTTP_400_BAD_REQUEST)
        if country is None:
            return Response({"message":"There should b a country"}, status=status.HTTP_400_BAD_REQUEST)
        if postal is None:
            return Response({"message":"There should b a postal code"}, status=status.HTTP_400_BAD_REQUEST)
        if phone is None:
            return Response({"message":"There should b a phone number"}, status=status.HTTP_400_BAD_REQUEST)
        
        if default==True:
            addr=Address()
            addr.user=User.objects.get(id=user)
            addr.first_name=first_name
            addr.last_name=last_name
            addr.company=company
            addr.address1=address1
            addr.address2=address2
            addr.city=city
            addr.country=country
            addr.postal=postal
            addr.phone=phone
            addr.default=True
            addr.save()
            addr1=Address.objects.get(user=addr.user,first_name=addr.first_name,
            last_name=addr.last_name,company=addr.company,address1=addr.address1,
            city=addr.city,country=addr.country,postal=addr.postal,phone=addr.phone,
            default=addr.default)
            addr2=AddressSerializer(addr1)
            
            return Response({"message":"Default Address created","obj":addr2.data}, status=status.HTTP_200_OK)
        else:
            addr=Address()
            addr.user=User.objects.get(id=user)
            addr.first_name=first_name
            addr.last_name=last_name
            addr.company=company
            addr.address1=address1
            addr.address2=address2
            addr.city=city
            addr.country=country
            addr.postal=postal
            addr.phone=phone
            addr.default=False
            addr.save()
            addr1=Address.objects.get(user=addr.user,first_name=addr.first_name,
            last_name=addr.last_name,company=addr.company,address1=addr.address1,
            city=addr.city,country=addr.country,postal=addr.postal,phone=addr.phone,
            default=addr.default)
            addr2=AddressSerializer(addr1)
            return Response({"message":"Address created","obj":addr2.data}, status=status.HTTP_200_OK)

        return Response({"message":"Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)




class AddressUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes=[]
    queryset=Address.objects.all()

class UpdateAddressView(APIView):
    permission_classes=[]
    def post(self, request, *args, **kwargs):
        print(request.data)
        user=request.data.get('user',None)
        add_id=request.data.get('id',None)
        first_name=request.data.get('first_name',None)
        last_name=request.data.get('last_name',None)
        company=request.data.get('company',None)
        address1=request.data.get('address1',None)
        address2=request.data.get('address2',None)
        city=request.data.get('city',None)
        country=request.data.get('country',None)
        postal=request.data.get('postal',None)
        phone=request.data.get('phone',None)
        default=request.data.get('default',None)
        if user is None:
            return Response({"message":"There should b a user."}, status=status.HTTP_400_BAD_REQUEST)
        if add_id is None:
            return Response({"message":"There should b an id."}, status=status.HTTP_400_BAD_REQUEST)
        if first_name is None:
            return Response({"message":"There should b a first name."}, status=status.HTTP_400_BAD_REQUEST)
        if last_name is None:
            return Response({"message":"There should b a last name."}, status=status.HTTP_400_BAD_REQUEST)
        if company is None:
            return Response({"message":"There should b a company."}, status=status.HTTP_400_BAD_REQUEST)
        if address1 is None:
            return Response({"message":"There should b a address1"}, status=status.HTTP_400_BAD_REQUEST)
        if city is None:
            return Response({"message":"There should b a city"}, status=status.HTTP_400_BAD_REQUEST)
        if country is None:
            return Response({"message":"There should b a country"}, status=status.HTTP_400_BAD_REQUEST)
        if postal is None:
            return Response({"message":"There should b a postal code"}, status=status.HTTP_400_BAD_REQUEST)
        if phone is None:
            return Response({"message":"There should b a phone number"}, status=status.HTTP_400_BAD_REQUEST)
        obj=Address.objects.get(id=add_id)
        if obj:
            obj.first_name=first_name
            obj.last_name=last_name
            obj.company=company
            obj.address1=address1
            obj.address2=address2
            obj.city=city
            obj.country=country
            obj.postal=postal
            obj.phone=phone
            obj.default=default
            obj.save()
            return Response(status=status.HTTP_200_OK)
        return Response({"message":"No item is updated. Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)

class PaymentView(APIView):
    permission_classes=[]
    def post(self,request, *args, **kwargs):
        user=request.data.get('user')
        order = Order.objects.get(user=user, ordered=False)
        
        token = request.data.get('stripeToken')
        print(order)
        print(token)
        print(order.total)
        amount = int(order.total)*100
        

        try:
                # charge once off on the token
            charge = stripe.Charge.create(
                amount=amount,  # cents
                currency="usd",
                source=token
            )
            print(charge)


            # create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = User.objects.get(id=user)
            payment.amount = int(order.total)
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            order.save()

            return Response(status=status.HTTP_200_OK)

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            return Response({"message":f"{err.get('message')}"},status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            # messages.warning(self.request, "Rate limit error")
            return Response({"message": "Rate limit error"},status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            # messages.warning(self.request, "Invalid parameters")
            return Response({"message":  "Invalid parameters"},status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            # messages.warning(self.request, "Not authenticated")
            return Response({"message":  "Not authenticated"},status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            # messages.warning(self.request, "Network error")
            return Response({"message":  "Network error"},status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return Response({"message":  "Something went wrong. You were not charged. Please try again."},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # send an email to ourselves
            print(e)
            return Response({"message":   "A serious error occurred. We have been notifed."},status=status.HTTP_400_BAD_REQUEST)

        return Response({"message":  "Invalid data received"},status=status.HTTP_400_BAD_REQUEST)