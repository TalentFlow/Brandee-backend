from rest_framework.routers import DefaultRouter
from products.api.views import ProductWishlistViewset
 
 
wishlist_router = DefaultRouter()
 
wishlist_router.register('', ProductWishlistViewset),