from csv import list_dialects
from django.contrib import admin
from .models import MainCategoryModel,SubCategoryModel,ProductModel,Cart,Address,Myorder,Contact

# Register your models here.

@admin.register(MainCategoryModel)
class MainCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["info","image","name"][::-1]


@admin.register(SubCategoryModel)
class SubCategoryModelAdmin(admin.ModelAdmin):
    list_display = ["info","image","name"][::-1]


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["total_price", "status", "info", "sell_price", "discounted_price", "discount", "og_price", "image3", "image2", "image1", "image", "name", "scate", "mcate"][::-1]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["quantity","product","user"][::-1]


@admin.register(Address)    
class AddressAdmin(admin.ModelAdmin):
    list_display = ["name","lastname","address","phone_number","city"][::-1]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name","email","phone_number","subject"][::-1]    


@admin.register(Myorder)
class MyorderAdmin(admin.ModelAdmin):
    list_display = ["status", "date" , "quantity", "product", "address", "user"][::-1]

