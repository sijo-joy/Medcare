from django.contrib.auth.models import User
from django import forms
from . import models
from meduser.models import Donations, ProductImage, Cart, Products, ProductsCategory
import re
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):
    product_category_text = forms.CharField()
    user_name = forms.CharField()
    donation = forms.IntegerField()
    mobile = forms.CharField()
    email = forms.CharField()
    product_category_text = forms.CharField()
    check_box = forms.BooleanField(required=False)
    files = forms.ImageField(required=False, widget=forms.FileInput(attrs={'multiple': 'true'}))

    class Meta:
        model = Products
        fields = ("name", "Description", "files", "check_box", "user_name", "mobile", "product_category_text", "email", "product_category", "expiry_date", "deposite_Amount", 'product_category', 'product_category_text')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_mobile(self):
        mobile = str(self.cleaned_data.get("mobile"))
        rule = re.compile(r'[89]\d{8}$')

        if not rule.search(mobile):
            msg = u"Invalid mobile number."
            raise forms.ValidationError(msg)
        return mobile

    def save(self, commit=True):
        product_name = self.cleaned_data["name"]
        product_category = self.cleaned_data["product_category"]
        Description = self.cleaned_data["Description"]
        deposite_Amount = self.cleaned_data["deposite_Amount"]
        product_category_text = self.cleaned_data["product_category_text"]

        donation_id = self.cleaned_data['donation']
        donation = Donations.objects.filter(pk=donation_id)[0]
        donation.approved = True
        if not donation.product:
            category = ''
            if not product_category and product_category_text:
                category = ProductsCategory.objects.get_or_create(name=product_category_text)[0]
                donation.product_category = category
            elif product_category:
                category = donation.product_category
            product = Products.objects.create(deposite_Amount=deposite_Amount, name=product_name, product_category=category, Description=Description ,donated_user=donation.donated_user,available=True ,active=True)
            for image in donation.productimage_set.all():
                image.product = product
                image.save()
            donation.product = product
            donation.save()
        return product