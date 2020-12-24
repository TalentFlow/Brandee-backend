from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from .views import (ProductListView , ProductGetView, ProductPhotosListView,
 ProductSingleGetView,HomePhotosListView,AddToCartView,DeleteItemFromCart,
 OrderItemsListView,CartItemQuantityUpdateView,OrderListView,WishlistGetView,
 NavbarMobileView,AddressListView,AddressCreateView,AddressUpdateDeleteView,UpdateAddressView,PaymentView)
from products.api.routes.wishlistroute import wishlist_router

urlpatterns = [
    path('products/', ProductListView.as_view(), name="product-list"),
    path('photos/', ProductPhotosListView.as_view()),
    path('home-photos/', HomePhotosListView.as_view()),
    path('product/wishlist/', include(wishlist_router.urls)),
    path('wishlist/', WishlistGetView.as_view()),
    path('products/getfor/', ProductGetView.as_view()),
    path('product-detail/', ProductSingleGetView.as_view()),
    path('add-to-cart/', AddToCartView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('order-items/', OrderItemsListView.as_view()),
    path('order-items/update/', CartItemQuantityUpdateView.as_view()),
    path('order-items/<pk>/delete/', DeleteItemFromCart.as_view()),
    path('navbar-mobile/', NavbarMobileView.as_view()),
    path('addresses/', AddressListView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/<pk>/', AddressUpdateDeleteView.as_view()),
    path('upd/address/', UpdateAddressView.as_view()),
    path('checkout/', PaymentView.as_view()),
]
