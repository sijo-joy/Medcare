from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from meduser.models import Cart
from . import models
import re


class RegisterForm(UserCreationForm):
    fullname = forms.CharField(label ="First name")
    mobile = forms.CharField(label="10 Digit Mobile Number")

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        rule = re.compile(r'[089]\d{9}$')

        if not rule.search(mobile):
            msg = u"Invalid mobile number."
            raise forms.ValidationError(msg)
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists")
        return email

    class Meta:
        model = User
        fields = ("username", "fullname", "mobile", 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        last_name = ""
        first_name = ""
        if len(self.cleaned_data["fullname"].split()) == 2:
            first_name, last_name = self.cleaned_data["fullname"].split()
        elif len(self.cleaned_data["fullname"].split()) == 1:
            first_name = self.cleaned_data["fullname"]
        mobile = self.cleaned_data["mobile"]
        user.first_name = first_name
        if last_name != "":
            user.last_name = last_name
        if commit:
            user.save()
        models.UserExtra.objects.create(user=user, mobile=mobile)
        Cart.objects.create(user_cart=user)
        return user