from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType

from .models import Donations, Products, ProductsCategory, ProductImage, Cart, CartItems, Company, Currency, \
    ContactMessages


# Register your models here.
class DoantionInline(admin.StackedInline):
    model = ProductImage
    can_delete = True
    verbose_name_plural = 'Images'

def unapprove(modeladmin,request,queryset):
    queryset.update(approved=False)

def approve(modeladmin,request,queryset):

    donation = queryset.get()
    if donation.approved == False :
        donation.approved = True
        if not donation.product:
            category = ''
            if not donation.product_category and donation.product_category_text:
                category = ProductsCategory.objects.get_or_create(name=donation.product_category_text)
                donation.product_category = category
            elif donation.product_category:
                category = donation.product_category
            product = Products.objects.create(name=donation.product_name, product_category=category, Description=donation.Description,donated_user=donation.donated_user,available=True ,active=True)
            for image in donation.productimage_set.all():
                image.product = product
                image.save()
            donation.product = product
            donation.save()

class DonationAdmin(UserAdmin):
    inlines = (DoantionInline,)
    actions = (approve, unapprove,)
    list_display = ('product_name','user_name','product_category','approved')
    search_fields = ('product_name','user_name')
    readonly_fields = ('created_date',)
    ordering = ('created_date',)

    filter_horizontal = ()
    list_filter = ('approved',('donated_user', admin.RelatedOnlyFieldListFilter),('product_category', admin.RelatedOnlyFieldListFilter),)
    fieldsets = ()

class ProductInline(admin.StackedInline):
    model = ProductImage
    can_delete = True
    verbose_name_plural = 'Images'

def activate(modeladmin,request,queryset):
    queryset.update(active=True)

def deactivate(modeladmin,request,queryset):
    queryset.update(active=False)


class ProductAdmin(UserAdmin):
    inlines = (ProductInline,)
    actions = (activate, deactivate,)
    list_display = ('name','product_category','donated_user','available','active')
    search_fields = ('name','product_category')
    readonly_fields = ('created_date',)
    ordering = ('created_date',)

    filter_horizontal = ()
    list_filter = ('active','available',('donated_user', admin.RelatedOnlyFieldListFilter),('product_category', admin.RelatedOnlyFieldListFilter),)
    fieldsets = ()



class CartInline(admin.TabularInline):
    model = CartItems
    can_delete = True
    verbose_name_plural = 'Items'

class CartAdmin(admin.ModelAdmin):
    inlines = (CartInline,)
    list_display = ('user_cart','total',)


admin.site.register(Donations, DonationAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(ProductsCategory)
# admin.site.register(ProductImage)
admin.site.register(ContactMessages)
admin.site.register(Cart, CartAdmin)

admin.site.register(Company)
admin.site.register(Currency)
