from django.contrib.auth.models import User
from django import forms
from . import models
from meduser.models import Donations, ProductImage, Cart, ProductsCategory
import re
from multiupload.fields import MultiFileField


class BookForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookForm, self).__init__(*args, **kwargs)

    def clean(self):
        cart = Cart.objects.filter(user_cart=self.user)[0]
        cart_items = cart.cartitems.all()
        for item in cart_items:
            if not item.product.available:
                raise forms.ValidationError("Remove unavailable product from cart to continue.")
        return cart




class ChangeDetailsForm(forms.ModelForm):
    mobile = forms.CharField(label="10 Digit Mobile Number")
    fullname = forms.CharField()

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeDetailsForm, self).__init__(*args, **kwargs)

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        rule = re.compile(r'[089]\d{9}$')

        if not rule.search(str(mobile)) or len(mobile) != 10:
            msg = u"Invalid mobile number."
            raise forms.ValidationError(msg)
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email ).exclude(pk=self.user.id).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = self.user
        mobile = self.cleaned_data.get("mobile")
        email = self.cleaned_data["email"]
        last_name = ""
        first_name = ""
        if len(self.cleaned_data["fullname"].split()) == 2:
            first_name, last_name = self.cleaned_data["fullname"].split()
        elif len(self.cleaned_data["fullname"].split()) == 1:
            first_name = self.cleaned_data["fullname"]
        user.first_name = first_name
        user.email = email
        if last_name != "":
            user.last_name = last_name
        user.userextra.mobile = str(mobile)
        user.userextra.save()
        user.save()
        return user



class DonationForm(forms.ModelForm):
    filesss = forms.ImageField(widget=forms.FileInput(attrs={'multiple':'true'}))
    check_box = forms.BooleanField(required=False)

    class Meta:
        model = Donations
        fields = ("user_name", "filesss", "Description", "check_box", "mobile", "email", 'address', 'product_category', 'product_category_text', 'product_name')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DonationForm, self).__init__(*args, **kwargs)

    def clean_product_category(self):
        check_box = self.cleaned_data.get("check_box")
        product_category = self.cleaned_data.get("product_category")
        obj = ProductsCategory.objects.all()[0]
        if not product_category and not check_box:
            msg = "Select a product category"
            raise forms.ValidationError(msg)
        return product_category

    def clean_mobile(self):
        mobile = str(self.cleaned_data.get("mobile"))
        rule = re.compile(r'[89]\d{8}$')

        if not rule.search(mobile):
            msg = u"Invalid mobile number."
            raise forms.ValidationError(msg)
        return mobile

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email exists")
    #     return self.cleaned_data




    def save(self, commit=True):
        user_name = self.cleaned_data["user_name"]
        mobile = self.cleaned_data["mobile"]
        email = self.cleaned_data["email"]
        product_name = self.cleaned_data["product_name"]
        address = self.cleaned_data["address"]
        product_category = self.cleaned_data["product_category"]
        Description = self.cleaned_data["Description"]
        product_category_text = self.cleaned_data["product_category_text"]
        donation = models.Donations.objects.create(donated_user=self.user, user_name=user_name, product_name=product_name, mobile=mobile, email=email, address=address)
        if product_category:
            donation.product_category = product_category
        if Description:
            donation.Description = Description
        if product_category_text:
            donation.product_category_text = product_category_text
        donation.approved = False
        donation.save()
        return donation