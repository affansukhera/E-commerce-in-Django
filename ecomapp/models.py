from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class ParentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ChildCategory(models.Model):
    parent_category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, related_name='child_categories', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(ChildCategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    warranty = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def discounted_price(self):
        discount_amount = (float(self.discount_percentage) / 100) * float(self.price)
        discounted_price = float(self.price) - discount_amount
        return "{:.2f}".format(discounted_price)

    def formatted_price(self):
        return "{:.2f}".format(self.price)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_descriptions', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.description


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        if hasattr(self, 'user') and self.user is not None:
            return self.user.carts.filter(is_ordered=False).count()
        return 0


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.user.username


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    area_code = models.TextField(max_length=10)
    primary_phone = models.IntegerField()
    street_address = models.TextField(max_length=100, default='')
    zip_code = models.IntegerField(default=0)
    business_address = models.BooleanField(default=False, null=True, blank=True)
