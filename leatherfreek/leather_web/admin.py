from django.contrib import admin

# Register your models here.

from .models import Display_Product , ProductImage , Color , Catagory , Design_Catagory , Home_Product , Volume_Description

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

