from django.db import models
from django.contrib.auth import settings
from cloudinary.models import CloudinaryField
import cloudinary
from django.db.models import Q
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, pre_save,pre_delete
from .utils import unique_slug_generator,unique_order_id_generator
from django_countries.fields import CountryField


#   General Catagory

SHOES='SHOES'
BAGS='BAGS'
BOUTIQUE='BOUTIQUE'
GLASSES='GLASSES'
MATERNITY_STORE='MATERNITY_STORE'
JEWELLERY='JEWELLERY'
MAKE_UP='MAKE_UP'
FITNESS_ACCESSORIES='FITNESS_ACCESSORIES'
FITNESS_APPARELS='FITNESS_APPARELS'
UNDERGARMENTS='UNDERGARMENTS'
STUFF_CATAGORY = [
    (SHOES, 'Shoes'),
    (BAGS, 'Bags'),
    (BOUTIQUE, 'Boutique'),
    (MATERNITY_STORE, 'Maternity-Store'),
    (GLASSES, 'Glasses'),
    (MAKE_UP, 'Make-up'),
    (JEWELLERY, 'Jewellery'),
    (FITNESS_ACCESSORIES, 'Fitness-Accessories'),
    (FITNESS_APPARELS, 'Fitness-Apparel'),
    (UNDERGARMENTS, 'Under-garments'),
]

# Shoes Catagory 

SNEAKERS='SNEAKERS'
RUNNING_SHOES='RUNNING_SHOES'
PEEP_TOE_BOOTIES='PEEP_TOE_BOOTIES'
SANDLES_AND_SLIDES='SANDLES_AND_SLIDES'
WORKOUT_SHOES='WORKOUT_SHOES'
HIKING_AND_OUTDOOR='HIKING_AND_OUTDOOR'
GOLF='GOLF'
TENNIS='TENNIS'
VOLLEYBALL='VOLLEYBALL'
SOCCER='SOCCER'
BASKETBALL='BASKETBALL'
SKATEBOARDING='SKATEBOARDING'
SHOES_CATAGORY = [
    (SNEAKERS, 'Sneakers'),
    (RUNNING_SHOES, 'Running-Shoes'),
    (PEEP_TOE_BOOTIES,'Peep-Toe-Booties'),
    (SANDLES_AND_SLIDES, 'Sandles-And-Slides'),
    (WORKOUT_SHOES, 'Workout-Shoes'),
    (HIKING_AND_OUTDOOR, 'Hiking-And-Outdoor'),
    (GOLF, 'Golf'),
    (TENNIS, 'Tennis'),
    (VOLLEYBALL, 'VolleyBall'),
    (SOCCER, 'Soccer'),
    (BASKETBALL, 'BasketBall'),
    (SKATEBOARDING, 'SkateBoarding'),
]

# Bags Catagory

PURSES='PURSES'
CLUTCHES='CLUTCHES'
SHOULDER_BAGS='SHOULDER_BAGS'
RUCKSACKS='RUCKSACKS'
CROSS_BODY_BAGS='CROSS_BODY_BAGS'
BEACH_BAGS='BEACH_BAGS'
BUM_BAGS='BUM_BAGS'
SHOPPER_BAGS='SHOPPER_BAGS'
TOTE_BAGS='TOTE_BAGS'
TRAVEL_BAGS='TRAVEL_BAGS'
BAGS_CATAGORY = [
    (PURSES, 'Purses'),
    (CLUTCHES, 'Clutches'),
    (SHOULDER_BAGS, 'Shoulder-Bags'),
    (RUCKSACKS, 'Rucksacks'),
    (CROSS_BODY_BAGS, 'Cross-Body-Bags'),
    (BEACH_BAGS, 'Beach-Bags'),
    (BUM_BAGS, 'Bum-Bags'),
    (SHOPPER_BAGS, 'Shopper-Bags'),
    (TOTE_BAGS, 'Tote-Bags'),
    (TRAVEL_BAGS, 'Travel-Bags'),
]

#  Boutique Catagory

MAXI='MAXI'
BABYDOLL_DRESS='BABYDOLL_DRESS'
LITTLE_BLACK_DRESS='LITTLE_BLACK_DRESS'
FLORAL_DRESS='FLORAL_DRESS'
CASUAL_DRESS='CASUAL_DRESS'
MIDI_DRESS='MIDI_DRESS'
WRAP_DRESS='WRAP_DRESS'
SHIFT_DRESS='SHIFT_DRESS'
SOLID_DRESS='SOLID_DRESS'
T_SHIRT_DRESS='T_SHIRT_DRESS'
LACE_DRESS='LACE_DRESS'
COCKTAIL_DRESS='COCKTAIL_DRESS'
BOUTIQUE_CATAGORY = [
    (MAXI, 'Maxi-Dress'),
    (BABYDOLL_DRESS, 'Babydoll-Dress'),
    (LITTLE_BLACK_DRESS, 'Little-Black-Dress'),
    (FLORAL_DRESS, 'Floral-Dress'),
    (CASUAL_DRESS, 'Casual-Dress'),
    (MIDI_DRESS, 'Midi-Dress'),
    (WRAP_DRESS, 'Wrap-Dress'),
    (SHIFT_DRESS, 'Shift-Dress'),
    (SOLID_DRESS, 'Solid-Dress'),
    (T_SHIRT_DRESS, 'T-Shirt-Dress'),
    (LACE_DRESS, 'Lace-Dress'),
    (COCKTAIL_DRESS, 'Cocktail-Dress'),
]

#  Female JEWELLERY

RINGS='RINGS'
EARRINGS='EARRINGS'
NECKLACES='NECKLACES'
BRACELETS='BRACELETS'
JEWELLERY_CATAGORY=[
    (RINGS,'Rings'),
    (EARRINGS,'Earrings'),
    (NECKLACES,'Necklaces'),
    (BRACELETS,'Bracelets'),
]



# FITNESS APPAREL

EXERCISE_JACKETS='EXERCISE_JACKETS'
EXERCISE_TOPS='EXERCISE_TOPS'
SPORTS_BRA='SPORTS_BRA'
SWIM_SUITS='SWIM_SUITS'
WORKOUT_SHORTS_PAINTS='WORKOUT_SHORTS_PAINTS'
YOGA_APPAREL='YOGA_APPAREL'
FITNESS_APPARELS_CATAGORY=[
    (EXERCISE_JACKETS,'Exersice-Jackets'),
    (EXERCISE_TOPS,'Exersice-Tops'),
    (SPORTS_BRA,'Sports-Bra'),
    (SWIM_SUITS,'Swim-Suits'),
    (WORKOUT_SHORTS_PAINTS,'Workout-Shorts-Paints'),
    (YOGA_APPAREL,'Yoga-Apparel'),
]


# MATERNITY STORE

MATERNITY_BRA='MATERNITY_BRA'
BABY_SHOWER_DRESS='BABY_SHOWER_DRESS'
MATERNITY_BELTS='MATERNITY_BELTS'
MATERNITY_DRESS='MATERNITY_DRESS'
MATERNITY_PAINTS='MATERNITY_PAINTS'
MATERNITY_STORE_CATAGORY=[
    (MATERNITY_BRA,'Maternity-Bra'),
    (BABY_SHOWER_DRESS,'Baby-Shower-Dress'),
    (MATERNITY_BELTS,'Maternity-Belts'),
    (MATERNITY_DRESS,'Maternity-Dress'),
    (MATERNITY_PAINTS,'Maternity-Paints'),
]


# UNDER GARMENTS

BRAS='BRAS'
UNDERWEAR='UNDERWEAR'
PANTIES='PANTIES'
LINGERIE='LINGERIE'
SLEEP='SLEEP'
LOUNGE='LOUNGE'
UNDER_GARMENTS_CATAGORY=[
    (BRAS,'Bras'),
    (UNDERWEAR,'Underwear'),
    (PANTIES,'Panties'),
    (LINGERIE,'Lingerie'),
    (SLEEP,'Sleep'),
    (LOUNGE,'Lounge'),
]

# GLASSES

COMPUTER_GLASSES='COMPUTER_GLASSES'
SUNGLASSES='SUNGLASSES'
MUZZUCCHELLI_COLLECTION='MUZZUCCHELLI_COLLECTION'
METAL_COLLECTION='METAL_COLLECTION'
GLASSES_CATAGORY=[
    (COMPUTER_GLASSES,'Computer Glasses'),
    (SUNGLASSES,'Sunglasses'),
    (MUZZUCCHELLI_COLLECTION,'Muzzucchelli Collection'),
    (METAL_COLLECTION,'Metal Collection'),
]







class Sizes(models.Model):
    size=models.CharField(default=None, max_length=5)

    def __str__(self):
        return self.size

# class Prices(models.Model):
#     country=CountryField(blank_label='(select country)')
#     manufacturer_price=models.IntegerField(default=1)
#     new_price=models.IntegerField(default=1)
#     old_price=models.IntegerField(default=1)
#     first_shipping_price=models.IntegerField(default=1)
#     percentage_shipping_next_items=models.IntegerField(default=1)

#     def __str__(self):
#         return str(self.country)




    




class Product(models.Model):
    title= models.CharField(max_length=100,null=False)
    information= models.TextField()
    catagory=models.CharField(max_length=30,choices=STUFF_CATAGORY,default=SHOES)
    sizes=models.ManyToManyField(Sizes, blank=True)
    color=models.CharField(max_length=20,null=True,blank=True)
    shoes_catagory= models.CharField(max_length=30,choices=SHOES_CATAGORY,default=None,blank=True, null=True)
    bags_catagory= models.CharField(max_length=30,choices=BAGS_CATAGORY,default=None,blank=True, null=True)
    boutique_catagory= models.CharField(max_length=30,choices=BOUTIQUE_CATAGORY,default=None,blank=True, null=True)
    jewellery_catagory=models.CharField(max_length=30,choices=JEWELLERY_CATAGORY,default=None,blank=True, null=True)
    fitness_apparel_catagory=models.CharField(max_length=30,choices=FITNESS_APPARELS_CATAGORY,default=None,blank=True, null=True)
    maternity_store_catagory=models.CharField(max_length=30,choices=MATERNITY_STORE_CATAGORY,default=None,blank=True, null=True)
    under_garments_catagory=models.CharField(max_length=30,choices=UNDER_GARMENTS_CATAGORY,default=None,blank=True, null=True)
    glasses_catagory=models.CharField(max_length=30,choices=GLASSES_CATAGORY,default=None,blank=True, null=True)
    price_new=models.FloatField(default=0)
    price_old=models.FloatField(default=0)
    is_featured=models.BooleanField(default=False)
    is_new=models.BooleanField(default=False)
    on_sale=models.BooleanField(default=False)
    in_stock=models.IntegerField(default=1)
    slug=models.SlugField(blank=True, unique=True)
    Date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-Date']

    def __str__(self):
        return self.slug

def product_pre_save_reciever(sender,instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(product_pre_save_reciever, sender=Product)




class Wishlist(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    Date=models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        ordering = ['-Date']

    def __str__(self):
        return self.product.title

class ProductPhotos(models.Model):
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    img= CloudinaryField('image')
    # secondary= CloudinaryField(blank=True)
    is_featured=models.BooleanField(default=False)
    Date= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-Date']

    def __str__(self):
        return self.product.slug

def backup_product_image_path(sender,instance,*args,**kwrags):
    instance._current_img_file = instance.img
    print(instance.img)
post_init.connect(backup_product_image_path, sender=ProductPhotos)

# @receiver(post_init, sender= ProductPhotos)
# def backup_image_path(sender, instance, **kwargs):
#     instance._current_img_file = instance.img


@receiver(post_save, sender= ProductPhotos)
def delete_old_product_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_img_file'):
        print(instance._current_img_file)
        print(instance.img)
        if instance._current_img_file !="":
            if instance._current_img_file != instance.img:
                cloudinary.uploader.destroy(instance._current_img_file.public_id,invalidate=True)
            
        #     instance._current_img_file.delete(save=False)

@receiver(models.signals.post_delete, sender=ProductPhotos)
def auto_delete_product_photo_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding `Post` object is
    deleted."""
    if instance.img:
        print(instance.img.public_id)
        cloudinary.uploader.destroy(instance.img.public_id,invalidate=True)



class HomePhotos(models.Model):
    img= CloudinaryField('image')
    img_catagory=models.CharField(max_length=30,choices=STUFF_CATAGORY,default=None)
    Date= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-Date']

    def __str__(self):
        return self.img_catagory

    

    

@receiver(post_init, sender= HomePhotos)
def backup_image_path(sender, instance, **kwargs):
    instance._current_img_file = instance.img


@receiver(post_save, sender= HomePhotos)
def delete_old_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_img_file'):
        print(instance._current_img_file)
        print(instance.img)
        if instance._current_img_file !="":
            if instance._current_img_file != instance.img:
                cloudinary.uploader.destroy(instance._current_img_file.public_id,invalidate=True)
            
        #     instance._current_img_file.delete(save=False)

@receiver(models.signals.post_delete, sender=HomePhotos)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding `Post` object is
    deleted."""
    if instance.img:
        print(instance.img.public_id)
        cloudinary.uploader.destroy(instance.img.public_id,invalidate=True)

class OrderItems(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products=models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    ordered=models.BooleanField(default=False)
    quantity=models.IntegerField(default=1)
    size=models.CharField(max_length=10, null=True, blank=True)

    @property
    def price(self):
        price=self.products.price_new
        return price
    
    @property
    def total(self):
        price=self.products.price_new
        total=int(price) * int(self.quantity)
        return total

    def __str__(self):
        return f"{self.quantity} {self.products.title} by {self.user.email}"



class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=15)
    last_name=models.CharField(max_length=15)
    company=models.CharField(max_length=50,null=True,blank=True)
    address1=models.CharField(max_length=100)
    address2=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=20)
    country=CountryField(blank_label='(select country)')
    postal=models.CharField(max_length=10)
    phone=models.CharField(max_length=20)
    default=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"
    
    @property
    def name(self):
        return self.country.name

def address_pre_save_reciever(sender,instance, *args, **kwargs):
    user=instance.user
    first_name=instance.first_name
    last_name=instance.last_name
    company=instance.company
    address1=instance.address1
    address2=instance.address2
    city=instance.city
    country=instance.country
    postal=instance.postal
    phone=instance.phone
    default=instance.default
    if default==True:
            print("true")
            obj=Address.objects.filter(user=user,default=True)
            if obj.exists():
                print(obj)
                for item in obj:
                    item.default=False
                    item.save()

def address_pre_delete_reciever(sender,instance,*args,**kwrags):
    if instance.default==True:
        obj=Address.objects.filter(~Q(id=instance.id))
        if obj.count() >0:
            obj1=obj[0]
            if obj1:
                obj1.default=True
                obj1.save()
pre_save.connect(address_pre_save_reciever, sender=Address)
pre_delete.connect(address_pre_delete_reciever, sender=Address)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField()
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class Order(models.Model):
    order_id=models.CharField(max_length=120, blank=True)
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItems)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address=models.ForeignKey(Address,on_delete=models.SET_NULL, blank=True, null=True)
    ordered=models.BooleanField(default=False)
    date= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)

    

    @property
    def total(self):
        obj=self.items.all()
        total=0
        for obj1 in obj:
            total+=obj1.total
        return int(total)

    def __str__(self):
        return self.user.email

def order_pre_delete_reciever(sender,instance,*args,**kwrags):
    obj=instance

    if obj.items.count() > 0:
        for item in obj.items.all():
            item.delete()
pre_delete.connect(order_pre_delete_reciever, sender=Order)

def order_pre_save_reciever(sender,instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_id_generator(instance)
pre_save.connect(order_pre_save_reciever, sender=Order)
