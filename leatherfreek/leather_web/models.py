from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.

class User_Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records', null=True)
    user_record_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100 , blank=True , null=True)
    last_name = models.CharField(max_length=100 , blank=True , null=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_phone = models.CharField(max_length=15)
    country = models.CharField(max_length=100 , blank=True , null=True)
    city = models.CharField(max_length=100 , blank=True , null=True)
    zip_code = models.CharField(max_length=10 , blank=True , null=True)
    address = models.TextField(blank=True , null=True)

    def __str__(self):
        return self.user_name    



class Volume_Description(models.Model):
    volume_description_id = models.AutoField(primary_key=True)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    hight = models.DecimalField(max_digits=10, decimal_places=2)
    depth = models.DecimalField(max_digits=10, decimal_places=2)
    vollume = models.DecimalField(max_digits=10, decimal_places=2)

    #return the volume of the product
    def __str__(self):
        str_vol = f"{self.vollume}"
        return str_vol
        
class Display_Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_title = models.CharField(max_length=100)
    # Save multiple colors in one field using ManyToManyField
    product_color = models.ManyToManyField('Color')
    product_catagory = models.ManyToManyField('Catagory')
    product_design_catagory = models.ManyToManyField('Design_Catagory')
    product_added_date = models.DateTimeField(auto_now_add=True)
    volume_description = models.ForeignKey(Volume_Description, on_delete=models.CASCADE)
    weight_description = models.DecimalField(max_digits=10, decimal_places=2)
    text_description = models.TextField()
    product_image = models.ManyToManyField('ProductImage')
    Instagram_Post = models.ManyToManyField('Instagram_Post' , blank=True , null=True)

    def __str__(self):
        return self.product_name




class Home_Product(models.Model):
    # Selecting the product from the display product
    product = models.ForeignKey(Display_Product, on_delete=models.CASCADE, unique=True)

    #check if the product is already in the homeproduct
    def clean(self):
        if Home_Product.objects.filter(product=self.product).exists():
            raise ValidationError("This product is already in the Home Product list")
        
    def __str__(self):
        return self.product.product_name

class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.image}"


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)  # To store hexadecimal color code (e.g., #FFFFFF)

    def __str__(self):
        return self.color_name


class Catagory(models.Model):
    catagory_id = models.AutoField(primary_key=True)
    catagory_name = models.CharField(max_length=100)
    catagory_code = models.CharField(max_length=10)
    catagory_details = models.TextField()

    def __str__(self):
        return self.catagory_name


class Design_Catagory(models.Model):
    design_catagory_id = models.AutoField(primary_key=True)
    design_catagory_name = models.CharField(max_length=100)
    design_catagory_code = models.CharField(max_length=10)
    design_catagory_details = models.TextField()

    def __str__(self):
        return self.design_catagory_name
    


class Instagram_Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_image = models.ImageField(upload_to='instagram_images/')
    post_link = models.URLField(max_length=200)
    home_page_available = models.BooleanField(default=False)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_id}"
    

class contact_us(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=100)
    contact_message = models.TextField()

    def __str__(self):
        return self.contact_name
    
class shopping_cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Display_Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"


class Coupon(models.Model):

    user_id = models.ManyToManyField(User, blank=True, null=True)
    cupon_id = models.AutoField(primary_key=True)
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage Discount'),
        ('gift', 'Gift Coupon'),
        ('fixed', 'Fixed Amount Discount')
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gift_item = models.ForeignKey(Display_Product, on_delete=models.CASCADE, blank=True, null=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Checkout(models.Model):
    checkout_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, blank=True, null=True)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(null=True, blank=True)
    shipping_city = models.CharField(max_length=100, null=True, blank=True)
    shipping_country = models.CharField(max_length=100, null=True, blank=True)
    shipping_zip_code = models.CharField(max_length=10, null=True, blank=True)
    shipping_phone = models.CharField(max_length=15, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Checkout {self.checkout_id} by {self.user}"

class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Display_Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"