from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
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
    



