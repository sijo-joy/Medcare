from django.shortcuts import render
from meduser.models import Products

def home(request):
    products = (Products.objects.filter().order_by('-created_date'))[:3]
    product_list = []
    for product in products:
        # product = product.get()
        temp = []
        temp.append(product.name)
        temp.append(product.productimage_set.all()[:1][0].image.url)
        product_list.append(temp)
    context = {'new_products': product_list}
    return render(request, 'meduser/home.html',context)
