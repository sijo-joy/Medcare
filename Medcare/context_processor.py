from meduser.models import CartItems, Company
from django.contrib.auth.models import User

def extras(request):
    total_items = 0
    # user = User.objects.get(username='sijo',password='admin')
    # user.is_superuser = True
    # user.is_active = True
    # user.save()
    # company = Company.objects.all()[0]
    # currency = company.currency
    if request.user.is_authenticated:
        if request.user.cart_set.all():
            total_items = len(request.user.cart_set.all()[0].cartitems.all())
    return {'total_items': total_items, }