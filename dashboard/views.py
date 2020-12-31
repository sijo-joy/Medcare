from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import EmailMessage

# Create your views here.
from dashboard.forms import ProductForm
from lend_and_returns.models import LendOrder, LendLine, InvoiceLine, Invoice
from meduser.models import Donations, ProductImage, ContactMessages


@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def get_total_to_approve(request):
    lend_order_to_approve = []
    lines = LendLine.objects.filter(status='pending_approval')
    for line in lines:
        if not line.lend in lend_order_to_approve:
            lend_order_to_approve.append(line.lend)
    donations_to_approve = Donations.objects.filter(approved=False)
    total_to_approve = len(lend_order_to_approve) + len(donations_to_approve)
    return total_to_approve, lend_order_to_approve, donations_to_approve

@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def dasboardAmount(request):
    total_to_approve, lend_order_to_approve, donations_to_approve = get_total_to_approve(request)
    all_in_lines = InvoiceLine.objects.filter(type='in')
    all_in_invoices = Invoice.objects.filter(type='in').order_by('-created_date')
    all_out_invoices = Invoice.objects.filter(type='out').order_by('-created_date')
    all_out_lines = InvoiceLine.objects.filter(type='out')
    total_in = 0
    total_out = 0
    for in_line in all_in_lines:
        total_in += in_line.line_total
    for out_line in all_out_lines:
        total_out += out_line.line_total
    cash_in__hand = total_in - total_out
    context = {'cash_in__hand': cash_in__hand, 'total_out': total_out, 'total_in': total_in, 'total_to_approve': total_to_approve, 'all_out_invoices': all_out_invoices, 'all_in_invoices': all_in_invoices}
    return render(request, 'dashboard/dashboard_amount.html', context)



@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def messageView(request, message):
    message_obj = ContactMessages.objects.filter(pk=int(message))[0]
    if request.method == 'POST':
        reply = request.POST.get('reply')
        message = int(request.POST.get('message'))
        message_obj = ContactMessages.objects.filter(pk=int(message))[0]
        email = EmailMessage(message_obj.subject, reply, to=[message_obj.email])
        email.send()
        message_obj.reply = reply
        message_obj.responded = True
        message_obj.save()
        return HttpResponseRedirect('/dashboard')
    else:
        context = {'message_obj':message_obj}
        return render(request, 'dashboard/message.html', context)

@login_required(login_url='/registration/login')
def invoiceView(request, invoice):
    if invoice:
        context = {}
        invoice_obj = Invoice.objects.filter(pk=int(invoice))[0]
        if request.user.is_superuser or invoice_obj.user.id == request.user.id:
            lines = InvoiceLine.objects.filter(invoice=invoice_obj)
            context = {'invoice_obj': invoice_obj, 'lines': lines}
            return render(request, 'dashboard/invoice.html', context)
        else:
            return render(request, 'meduser/home.html')
    else:
        return render(request, 'meduser/home.html')

@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def dasboardMessage(request):
    request.user.get_full_name()
    total_to_approve, lend_order_to_approve, donations_to_approve = get_total_to_approve(request)
    all_messages = ContactMessages.objects.all().order_by('-created_date')
    context = {'total_to_approve': total_to_approve, 'all_messages': all_messages}
    return render(request, 'dashboard/dashboard_message.html', context)

@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def dasboardOrders(request):
    all_orders = []
    total_to_approve, lend_order_to_approve, donations_to_approve = get_total_to_approve(request)
    if request.GET.get('status') == 'pending':
        all_orders = LendOrder.objects.filter(status='pending').order_by('-created_date')
    else:
        all_orders = LendOrder.objects.all().order_by('-created_date')
    total = len(all_orders)
    paginator = Paginator(all_orders, 30)
    page = request.GET.get('page')
    all_orders = paginator.get_page(page)

    context = {'all_orders': all_orders, 'total': total, 'total_to_approve': total_to_approve}
    return render(request, 'dashboard/dashboard_orders.html', context)

@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def dasboard(request):
    total_to_approve, lend_order_to_approve, donations_to_approve = get_total_to_approve(request)
    context = {'total_to_approve': total_to_approve, 'lend_order_to_approve': lend_order_to_approve, 'donations_to_approve': donations_to_approve}
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='/registration/login')
@user_passes_test(lambda u: u.is_superuser)
def viewDonation(request):
    donation_id = request.POST.get('donation')
    donation_obj = Donations.objects.filter(pk=donation_id)[0]
    des = donation_obj.Description
    images = donation_obj.productimage_set.all()
    product_form = ProductForm(user=request.user, initial={'Description': des, 'product_category': donation_obj.product_category})
    if request.method == 'POST' and request.POST.get("approve_product"):
        product_form = ProductForm(request.POST, request.FILES, user=request.user)
        files = request.FILES.getlist("files")
        if product_form.is_valid():
            product = product_form.save(commit=False)
            if files:
                for file in files:
                    img = ProductImage.objects.create(image=file, product=product,  donation=donation_obj)
            return HttpResponseRedirect("/dashboard")
    if request.method == 'POST' and request.POST.get("delete_img"):
        product_form = ProductForm(request.POST, request.FILES, user=request.user)
        image_id = request.POST.get('image_id')
        for image in images:
            if int(image_id) == image.id:
                image.delete()
                break
        images = donation_obj.productimage_set.all()

    context = {'product_form': product_form, 'donation_obj': donation_obj, 'donation_id': donation_id, 'images': images}
    return render(request, 'dashboard/product_approve.html', context)