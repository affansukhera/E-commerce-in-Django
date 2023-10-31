from django.contrib import admin
from .models import ParentCategory, ChildCategory, Product, ProductDescription, ProductImage,Contact, Cart, UserProfile, ShippingAddress


@admin.register(ParentCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']


@admin.register(ChildCategory)
class ChildCategoryAdmin(admin.ModelAdmin):
    list_display = ['parent_category', 'name', 'description', 'is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'slug',  'price', 'in_stock', 'category', 'is_active', 'is_featured', 'discount_percentage', 'warranty', 'image']


@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'description', 'image']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company_name',  'area_code', 'primary_phone', 'street_address', 'zip_code', 'business_address']

