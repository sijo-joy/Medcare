from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from lend_and_returns.models import LendOrder
from .forms import DonationForm, ChangeDetailsForm, BookForm
from .models import ProductImage, Products, ProductsCategory, Cart, CartItems, Company, ContactMessages
from registration import views as reg_views
from django.forms import modelformset_factory
from django.contrib import messages
from datetime import date


def home(request):
    return render(request, 'meduser/home.html')

def about(request):
    return render(request, 'meduser/about.html')

def contact(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        ContactMessages.objects.create(message=message,name=name,email=email,subject=subject,responded=False)
    return render(request, 'meduser/contact.html')


def products(request, category=None):
    product_categories_dic = {}
    products = []
    context = {}
    product_categories = (ProductsCategory.objects.filter().order_by('name'))
    sort = request.GET.get('sort')
    if request.method == 'POST':
        query = request.POST.get('query')
        if sort:
            if sort == "name":
                temp = {'default_sort': 1}
                context = {**context, **temp}
                products = (Products.objects.filter(name__icontains=query, active=True).order_by('name'))
            elif sort == "new":
                temp = {'default_sort': 2}
                context = {**context, **temp}
                products = (Products.objects.filter(name__icontains=query, active=True).order_by('-created_date'))
        else:
            products = (Products.objects.filter(name__icontains=query, active=True).order_by('name'))
    elif sort:
        if sort == "name":
            temp = {'default_sort': 1}
            context = {**context, **temp}
            products = (Products.objects.filter(active=True).order_by('name'))
        elif sort == "new":
            temp = {'default_sort': 2}
            context = {**context, **temp}
            products = (Products.objects.filter(active=True).order_by('-created_date'))

    else:
        products = (Products.objects.filter(active=True).order_by('name'))
    for categorie in product_categories:
        product_categories_dic[categorie] = 0
    all_products = (Products.objects.filter(active=True).order_by('name'))
    for product in all_products:
        product_categories_dic[product.product_category] = 1 if not product_categories_dic.get(
            product.product_category) else product_categories_dic.get(product.product_category) + 1

    if category:
        temp = {'current_category': int(category)}
        context = {**context, **temp}
        product_category = ProductsCategory.objects.filter(pk=category)
        products = Products.objects.filter(product_category=product_category.get()).order_by('name')
    product_list = []
    print(category)
    for product in products:
        temp = []
        temp.append(product.name)
        temp.append(product.productimage_set.all()[:1][0].image.url)
        temp.append(product)
        product_list.append(temp)
    paginator = Paginator(product_list, 30)
    page = request.GET.get('page')
    product_lists = paginator.get_page(page)
    temp = {'products': product_lists, 'total': len(product_list), 'product_categories': list(product_categories_dic.items())}
    context = {**context, **temp}
    return render(request, 'meduser/products.html', context)


@login_required(login_url='/registration/login')
def profilePage(request):
    context ={}
    changePage = ChangeDetailsForm(user=request.user)
    changeform = PasswordChangeForm(request.user)

    if request.method == 'POST' and request.POST.get("save_profile"):
        changePage = ChangeDetailsForm(request.POST, user=request.user)
        if changePage.is_valid():
            post_form = changePage.save(commit=False)
            return HttpResponseRedirect("/")
        else:
            print(changePage.errors)
    if request.method == 'POST' and request.POST.get("save_changes"):
        changeform = PasswordChangeForm(request.user, request.POST)
        if changeform.is_valid():
            user = changeform.save(commit=False)
            user.save()
            update_session_auth_hash(request, request.user)
            return HttpResponseRedirect("profile")
        else:
            temp = {'default': '3'}
            context = {**context, **temp}
            print(changePage.errors)
    full_name = request.user.first_name + " " + request.user.last_name
    lend_orders = LendOrder.objects.filter(user=request.user).order_by('-created_date')
    temp = {'full_name': full_name, 'changeForm': changePage, 'lend_orders': lend_orders, 'form': changeform}
    context = {**context, **temp}
    return render(request, 'meduser/profile.html', context)

@login_required(login_url='/registration/login')
def donationPage(request):
    donationPage = DonationForm(user=request.user)
    if request.method == 'POST':
        donationPage = DonationForm(request.POST, request.FILES, user=request.user)
        files = request.FILES.getlist("filesss")
        print(files)
        if donationPage.is_valid():
            post_form = donationPage.save(commit=False)
            if files:
                for file in files:
                    img = ProductImage.objects.create(image=file, donation=post_form)
            return HttpResponseRedirect("/")
        else:
            print(donationPage.errors)
    else:
        donationPage = DonationForm(user=request.user)
    context = {'form': donationPage}
    return render(request, 'meduser/donation.html', context)

@login_required(login_url='/registration/login')
def cart(request):
    user = request.user
    book_form = BookForm(user=request.user)
    cart = Cart.objects.get_or_create(user_cart=request.user)[0]
    cart_items = cart.cartitems.all()
    image_dict = {}
    total_items = len(cart_items)
    context = {'book_form': book_form, 'cart': cart, 'cart_items': cart_items, 'total_items': total_items, 'image_dict': image_dict}
    return render(request, 'meduser/cart.html', context)

@login_required(login_url='/registration/login')
def addToCart(request):
    expected_date = request.GET.get('date')
    product = int(request.GET.get('product'))
    product = Products.objects.filter(pk=product)[0]
    cart = Cart.objects.get_or_create(user_cart=request.user)[0]
    items = CartItems.objects.filter(cart=cart)
    for item in items:
        if item.product == product:
            return redirect("view_product", product=product.id)
    item = CartItems.objects.create(product=product, cart=cart, return_date=expected_date, line_total=product.deposite_Amount or 0.0)
    return redirect("products")

@login_required(login_url='/registration/login')
def removeFromCart(request, cart_item=None):
    cartitem = CartItems.objects.get(pk=cart_item)
    cartitem.delete()
    return redirect("cart")

def viewProduct(request, product=None):
    context = {}
    product = Products.objects.filter(pk=product)[0]
    images = product.productimage_set.all()
    img_list = []
    for image_ob in images:
        img_list.append(image_ob.image.url)
    des = product.Description
    today = date.today()
    if request.user.is_authenticated:
        if request.user.cart_set.all():
            items = CartItems.objects.filter(cart=request.user.cart_set.get())
            for item in items:
                if item.product == product:
                    temp = {'already_incart': 1}
                    context = {**context, **temp}
                    break
    temp = {'product': product, 'des': des, 'today': str(today), 'images': img_list}
    context = {**context, **temp}
    return render(request, 'meduser/product_details.html', context)