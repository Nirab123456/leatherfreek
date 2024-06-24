from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

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

    def __str__(self):
        return self.product_name


class Home_Product(models.Model):
    # Selecting the product from the display product
    product = models.ForeignKey(Display_Product, on_delete=models.CASCADE, unique=True)

    def clean(self):
        if Home_Product.objects.exists() and not self.pk:
            raise ValidationError("There can only be one home product.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Home Product: {self.product.product_name}'

class ProductImage(models.Model):
    product = models.ForeignKey(Display_Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.product_name} Image"


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

    def __str__(self):
        return self.catagory_name


class Design_Catagory(models.Model):
    design_catagory_id = models.AutoField(primary_key=True)
    design_catagory_name = models.CharField(max_length=100)
    design_catagory_code = models.CharField(max_length=10)

    def __str__(self):
        return self.design_catagory_name
