from django.contrib import admin

# Register your models here.

from .models import Display_Product , ProductImage , Color , Catagory , Design_Catagory , Home_Product , Volume_Description , Instagram_Post ,contact_us ,shopping_cart , User_Record

@admin.register(Home_Product)
class Home_ProductAdmin(admin.ModelAdmin):
    list_display = ('product',)
    list_filter = ('product',)
    ordering = ('product',)
    search_fields = ('product',)

@admin.register(Display_Product)
class Display_ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_price', 'product_title', 'product_added_date')
    list_filter = ('product_name', 'product_price', 'product_title', 'product_added_date')
    ordering = ('product_name',)
    search_fields = ('product_name', 'product_price', 'product_title', 'product_added_date')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'image')
    list_filter = ('image_id', 'image')
    ordering = ('image_id',)
    search_fields = ('image_id', 'image')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('color_id', 'color_name', 'hex_code')
    list_filter = ('color_name', 'hex_code')
    ordering = ('color_name',)
    search_fields = ('color_name', 'hex_code')

@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('catagory_id', 'catagory_name', 'catagory_code')
    list_filter = ('catagory_name', 'catagory_code')
    ordering = ('catagory_name',)
    search_fields = ('catagory_name', 'catagory_code')

@admin.register(Design_Catagory)
class Design_CatagoryAdmin(admin.ModelAdmin):
    list_display = ('design_catagory_id', 'design_catagory_name', 'design_catagory_code')
    list_filter = ('design_catagory_name', 'design_catagory_code')
    ordering = ('design_catagory_name',)
    search_fields = ('design_catagory_name', 'design_catagory_code')


@admin.register(Volume_Description)
class Volume_DescriptionAdmin(admin.ModelAdmin):
    list_display = ('volume_description_id', 'width' , 'hight' , 'depth' , 'vollume')
    list_filter = ('width' , 'hight' , 'depth' , 'vollume')
    ordering = ('width' , 'hight' , 'depth' , 'vollume')
    search_fields = ('width' , 'hight' , 'depth' , 'vollume')


@admin.register(Instagram_Post)
class Instagram_PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'post_image')
    list_filter = ('post_id', 'post_image')
    ordering = ('post_id',)
    search_fields = ('post_id', 'post_image')


@admin.register(contact_us)
class contact_usAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'phone_number', 'contact_email', 'contact_message')
    list_filter = ('contact_name', 'phone_number', 'contact_email', 'contact_message')
    ordering = ('contact_name',)
    search_fields = ('contact_name', 'phone_number', 'contact_email', 'contact_message')


@admin.register(shopping_cart)
class shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user', 'product', 'quantity')
    ordering = ('product',)
    search_fields = ('user', 'product', 'quantity')
    

@admin.register(User_Record)
class User_RecordAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name', 'user_name' , 'user_email' , 'user_phone' , 'country' , 'city' , 'zip_code')
    list_filter = ('first_name','last_name', 'user_name' , 'user_email' , 'user_phone' , 'country' , 'city' , 'zip_code')
    ordering = ('user_name',)
    search_fields = ('first_name','last_name', 'user_name' , 'user_email' , 'user_phone' , 'country' , 'city' , 'zip_code')
    




