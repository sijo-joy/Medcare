from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class Currency(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Currencies'


class Company(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email_support = models.CharField(max_length=50, null=True, blank=True)
    address1 = models.CharField(max_length=50, null=True, blank=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    pin = models.CharField(max_length=50, null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Companies'

class ProductsCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Products categories'

def get_image_filenames(instance, filename):
    product_name = instance.donation.product_name
    slug = slugify(product_name)
    return "product_images/%s-%s" % (slug, filename)

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/products/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}products/'.format(settings.MEDIA_URL),
)

class Products(models.Model):
    name = models.CharField(max_length=30)
    thumb_image = models.ImageField(verbose_name='Image', blank=True, null=True, upload_to=get_image_filenames, storage=image_storage,)
    Description = models.TextField(null=True, blank=True)
    product_category = models.ForeignKey(ProductsCategory, blank=True, null=True, on_delete=models.CASCADE)
    expiry_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    donated_user = models.ForeignKey(User, null=True, blank=True, related_name='donated_user', on_delete=models.CASCADE)
    available = models.BooleanField()
    active = models.BooleanField()
    current_user = models.ForeignKey(User, null=True, blank=True, related_name='current_user', on_delete=models.CASCADE)
    expected_return_date = models.DateField(blank=True, null=True)
    deposite_Amount = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2)
    length = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=2)
    weight = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=2)
    width = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Products'

class Cart(models.Model):
    user_cart = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user_cart.username)

    class Meta:
        verbose_name_plural = 'Cart'


class CartItems(models.Model):
    product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, null=True, blank=True, related_name='cartitems', on_delete=models.CASCADE)
    return_date = models.DateField(null=True,blank=True)
    edited_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    line_total = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return '{}'.format(self.product.name)

    class Meta:
        verbose_name_plural = 'Cart Items'

    def delete(self, *args, **kwargs):
        super(CartItems, self).delete(*args, **kwargs)
        cart_items = CartItems.objects.filter(cart=self.cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.line_total
        self.cart.total = total
        self.cart.save()

    def save(self, *args, **kwargs):
        super(CartItems, self).save(*args, **kwargs)
        cart_items = CartItems.objects.filter(cart=self.cart)
        total = 0
        for cart_item in cart_items:
            total += cart_item.line_total
        self.cart.total = total
        self.cart.save()


class Donations(models.Model):
    user_name = models.CharField(max_length=30)
    Description = models.TextField(null=True, blank=True,)
    product_name = models.CharField(max_length=30, null=True)
    mobile = models.DecimalField(max_digits=10, decimal_places=0)
    email = models.EmailField(max_length=255)
    address = models.TextField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    donated_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductsCategory, null=True, blank=True, on_delete=models.CASCADE)
    product_category_text = models.CharField(max_length=30, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(blank=True, null=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.user_name)}_{str(self.product_name)}'

    class Meta:
        verbose_name_plural = 'Donations'


def get_image_filename(instance, filename):
    product_name = instance.donation.product_name
    slug = slugify(product_name)
    return "product_images/%s-%s" % (slug, filename)

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/products/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}products/'.format(settings.MEDIA_URL),
)
class ProductImage(models.Model):
    donation = models.ForeignKey(Donations, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=get_image_filename, storage=image_storage,
                              verbose_name='Image', blank=True, null=True)

        # def __str__(self):
    #     return '{}'.format(self.product_name+" " + self.user_name)

    class Meta:
        verbose_name_plural = 'Product Images'

    # def delete(self, *args, **kwargs):
    #     super(ProductImage, self).delete(*args, **kwargs)
    #     cart_items = CartItems.objects.filter(cart=self.cart)
    #     total = 0
    #     for cart_item in cart_items:
    #         total += cart_item.line_total
    #     self.cart.total = total
    #     self.cart.save()

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)
        if self.product:
            self.product.thumb_image = ProductImage.objects.filter(product=self.product)[0].image
            self.product.save()


class ContactMessages(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=70)
    subject = models.CharField(max_length=30)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    responded = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Messages'