from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date
import json
from sample import PayPalClient
from paypalcheckoutsdk.payments import CapturesRefundRequest
# Create your views here.
from meduser.forms import BookForm
from meduser.models import Cart
from .models import LendOrder, LendLine, Invoice, InvoiceLine

# 1. Import the PayPal SDK client that was created in `Set up Server-Side SDK`.
from sample import PayPalClient
from paypalcheckoutsdk.payments import CapturesRefundRequest
import json
# 1. Import the PayPal SDK client created in `Set up Server-Side SDK` section.
from sample import PayPalClient
from paypalcheckoutsdk.orders import OrdersCaptureRequest


class CaptureOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """this sample function performs payment capture on the order.
  Approved order ID should be passed as an argument to this function"""

  def capture_order(self, order_id, debug=False):
    """Method to capture order usingd orer_id"""
    request = OrdersCaptureRequest(order_id)
    #3. Call PayPal to capture an order
    response = self.client.execute(request)
    amount_receved = 0
    for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
            amount_receved = capture.seller_receivable_breakdown.net_amount.value
    #4. Save the capture ID to your database. Implement logic to save capture to your database for future reference.
    # if debug:
    #   print ('Status Code: ', response.status_code)
    #   print ('Status: ', response.result.status)
    #   print ('Order ID: ', response.result.id)
    #   print ('Links: ')
    #   for link in response.result.links:
    #     print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
    #   print ('Capture Ids: ')
    #   for purchase_unit in response.result.purchase_units:
    #     for capture in purchase_unit.payments.captures:
    #       print ('\t', capture.id)
    #   print ("Buyer:")
    #   print ("\tEmail Address: {}\n\tName: {}\n\tPhone Number: {}".format(response.result.payer.email_address,
    #     response.result.payer.name.given_name + " " + response.result.payer.name.surname,
    #     response.result.payer.phone.phone_number.national_number))
    return response, amount_receved


"""This driver function invokes the capture order function.
Replace Order ID value with the approved order ID. """
if __name__ == "__main__":
  order_id = 'REPLACE-WITH-APPORVED-ORDER-ID'
  CaptureOrder().capture_order(order_id, debug=True)

class RefundOrder(PayPalClient):

  #2. Set up your server to receive a call from the client
  """Use the following function to refund an capture.
     Pass a valid capture ID as an argument."""
  def refund_order(self, capture_id, amount=None, full_refund=None, debug=False):
    request = CapturesRefundRequest(capture_id)
    request.prefer("return=representation")
    if full_refund:
        request.request_body(self.build_request_body_empty(amount))
    else:
        request.request_body(self.build_request_body(amount))
    #3. Call PayPal to refund an capture
    response = self.client.execute(request)
    if debug:
      print ('Status Code:', response.status_code)
      print ('Status:', response.result.status)
      print ('Order ID:', response.result.id)
      print ('Links:')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      json_data = self.object_to_json(response.result)
      print ("json_data: ", json.dumps(json_data,indent=4))
    return response

  """Request body for building a partial refund request.
     For full refund, pass the empty body.
     For more details, refer to the Payments API refund captured payment reference."""
  @staticmethod
  def build_request_body(amount):
    return \
      {
        "amount": {
          "value": str(amount),
          "currency_code": "EUR"
        }
      }

  @staticmethod
  def build_request_body_empty(amount):
      return \
      {

      }


"""This driver function invokes the refund capture function.
   Replace the Capture Id with a valid capture ID. """
    # if __name__ == "__main__":
    #     capture_id = &apos <REPLACE - WITH - VALID - CAPTURE - ID>
    #     '
    #     RefundOrder().refund_order(capture_id, debug=True)

@login_required(login_url='/registration/login')
def createLendOrder(request, cart, body):
    lend_order = LendOrder.objects.create(user=cart.user_cart, total=cart.total, transaction_id=body.get('capture_id'),order_id=body.get('id'))
    if float(body.get('amount')) == float(cart.total):
        lend_order.complete = True
        lend_order.save()
    return lend_order

@login_required(login_url='/registration/login')
def createLendOrderLines(request, lend_order, cart_items):
    lend_order_lines = []
    for cart_item in cart_items:
        lend_order_line = LendLine.objects.create(user=cart_item.cart.user_cart, lend=lend_order, product=cart_item.product,
                                          expected_return_date=cart_item.return_date, line_total=cart_item.line_total,)
        cart_item.product.available = False
        cart_item.product.expected_return_date = cart_item.return_date
        cart_item.product.save()
        lend_order_lines.append(lend_order_line)
    return lend_order_lines

@login_required(login_url='/registration/login')
def createInvoice(request, lend_order, body):
    invoice = Invoice.objects.create(user=lend_order.user, lend_order=lend_order, total=lend_order.total, type='in')
    return invoice


@login_required(login_url='/registration/login')
def createRefundInvoice(request, lend_order):
    invoice = Invoice.objects.get_or_create(user=lend_order.user, lend_order=lend_order, type='out')[0]
    return invoice

@login_required(login_url='/registration/login')
def createRefundInvoiceLine(request, lend_order, lend_order_line, invoice):
    invoice_line = InvoiceLine.objects.create(lend=lend_order, lend_line=lend_order_line, user_line=lend_order_line.user, product=lend_order_line.product, invoice=invoice,
                                      line_total=lend_order_line.line_total if lend_order_line.line_total > 0 else 0, type='out')
    return invoice_line

@login_required(login_url='/registration/login')
def createInvoiceLine(request, lend_order, lend_order_lines, invoice):
    invoice_lines = []
    for line in lend_order_lines:
        invoice_line = InvoiceLine.objects.create(lend=lend_order, lend_line=line, user_line=line.user, product=line.product, invoice=invoice,
                                          line_total=line.line_total, type='in')
        invoice_lines.append(invoice_line)
    return invoice_lines


@login_required(login_url='/registration/login')
def bookPay(request):
    body = json.loads(request.body)
    print(body)
    user = request.user
    book_form = BookForm(user=request.user)
    if request.method == 'POST':
        book_form = BookForm(request.POST, user=request.user)
        if book_form.is_valid():
            cart = Cart.objects.filter(user_cart=user)[0]
            cart_items = cart.cartitems.all()
            lend_order = createLendOrder(request, cart, body)
            lend_order_lines = createLendOrderLines(request, lend_order, cart_items)
            invoice = createInvoice(request, lend_order, body)
            invoice_lines = createInvoiceLine(request, lend_order, lend_order_lines,invoice)
            cart.delete()
            cart_items.delete()
            # capture = CaptureOrder()
            # response, amount_received = capture.capture_order(body.get('id'))
            # lend_order.amount_to_refund = amount_received
            # lend_order.total_received = amount_received
            # invoice.total_received = amount_received
            # lend_order.save()
            return render(request, 'meduser/home.html')
    cart = Cart.objects.filter(user_cart=user)[0]
    cart_items = cart.cartitems.all()
    image_dict = {}
    total_items = len(cart_items)
    context = {'book_form': book_form, 'cart': cart, 'cart_items': cart_items, 'total_items': total_items,
               'image_dict': image_dict}
    return render(request, 'meduser/cart.html',context)

@login_required(login_url='/registration/login')
def viewCheckout(request):
    user = request.user
    cart = Cart.objects.get_or_create(user_cart=request.user)[0]
    cart_items = cart.cartitems.all()
    image_dict = {}
    total_items = len(cart_items)
    context = {'cart': cart, 'cart_items': cart_items, 'total_items': total_items,
               'image_dict': image_dict}
    return render(request, 'lend_and_returns/checkout.html', context)

@login_required(login_url='/registration/login')
def viewOrder(request, lend_order_id=None):
    lend_id = request.POST.get('lend_order') if request.POST.get('lend_order') else lend_order_id
    lend_order = LendOrder.objects.filter(pk=lend_id)[0]
    invoices = Invoice.objects.filter(lend_order=lend_order.id)
    if lend_order.user.id == request.user.id or request.user.is_superuser:
        if request.method == 'POST'  and request.POST.get("update_date"):
            line_id = request.POST.get('line')
            new_date = request.POST.get('date')
            line_obj = LendLine.objects.filter(pk=line_id)[0]
            line_obj.expected_return_date = new_date
            line_obj.save()
            line_obj.product.expected_return_date = new_date
            line_obj.product.save()
        if request.method == 'POST' and request.POST.get("request_all"):
            lend_lines = lend_order.lendline.all().order_by('created_date')
            for line_obj in lend_lines:
                if line_obj.status == 'pending':
                    line_obj.status = 'pending_approval'
                    line_obj.save()
            lines = LendLine.objects.filter(lend=lend_id, status='pending')
            if not lines:
                lend_order.status = 'pending_approval'
                lend_order.save()

        if request.method == 'POST' and request.POST.get("return_line"):
            line_id = request.POST.get('line')
            line_obj = LendLine.objects.filter(pk=line_id)[0]
            if line_obj.status == 'pending':
                line_obj.status = 'pending_approval'
                line_obj.save()
                lines = LendLine.objects.filter(lend=lend_id, status='pending').exclude(pk=line_id)
                if not lines:
                    lend_order.status = 'pending_approval'
                    lend_order.save()
        if request.method == 'POST' and request.POST.get("approve_all"):
            lend_lines = lend_order.lendline.all().order_by('created_date')
            amount_to_refund = 0
            for line_obj in lend_lines:
                if line_obj.status == 'pending_approval':
                    line_obj.status = 'returned'
                    amount_to_refund += line_obj.line_total
                    line_obj.product.current_user = None
                    line_obj.returned_date = date.today()
                    invoice = createRefundInvoice(request, lend_order)
                    invoice_line = createRefundInvoiceLine(request, lend_order, line_obj, invoice)
                    line_obj.product.available = True
                    line_obj.product.save()
                    line_obj.save()
            paypal_obj = RefundOrder()
            print(amount_to_refund)
            trasaction = paypal_obj.refund_order(capture_id=lend_order.transaction_id, amount=amount_to_refund,
                                                 full_refund=False, debug=False)
            lines_pending = LendLine.objects.filter(lend=lend_id, status='pending')
            lines_pending_approval = LendLine.objects.filter(lend=lend_id, status='pending_approval')
            if lines_pending_approval:
                lend_order.status = 'pending_approval'
                lend_order.save()
            elif lines_pending:
                lend_order.status = 'pending'
                lend_order.save()
            else:
                lend_order.status = 'returned'
                lend_order.save()
        if request.method == 'POST' and request.POST.get("approve_return"):
            line_id = request.POST.get('line')
            line_obj = LendLine.objects.filter(pk=line_id)[0]
            if line_obj.status == 'pending_approval':
                amount_to_refund = line_obj.line_total
                print(amount_to_refund)
                invoice = createRefundInvoice(request, lend_order)
                paypal_obj = RefundOrder()
                trasaction = paypal_obj.refund_order(capture_id=lend_order.transaction_id, amount=amount_to_refund, full_refund=False, debug=False)
                line_obj.status = 'returned'
                line_obj.product.current_user = None
                line_obj.returned_date = date.today()
                line_obj.save()

                invoice_line = createRefundInvoiceLine(request, lend_order, line_obj, invoice)
                line_obj.product.available = True

                line_obj.product.save()
                lines_pending = LendLine.objects.filter(lend=lend_id, status='pending').exclude(pk=line_id)
                lines_pending_approval = LendLine.objects.filter(lend=lend_id, status='pending_approval').exclude(pk=line_id)
                if lines_pending_approval:
                    lend_order.status = 'pending_approval'
                    lend_order.save()
                elif lines_pending:
                    lend_order.status = 'pending'
                    lend_order.save()
                else:
                    lend_order.status = 'returned'
                    lend_order.save()
        if request.method == 'POST'  and request.POST.get("cancel_return"):
            line_id = request.POST.get('line')
            line_obj = LendLine.objects.filter(pk=line_id)[0]
            line_obj.status = 'pending'
            line_obj.save()
            lend_order.status = 'pending'
            lend_order.save()


        lend_lines = lend_order.lendline.all().order_by('created_date')
        context = {'lend_lines': lend_lines, 'lend_order': lend_order, 'invoices': invoices}
        return render(request, 'lend_and_returns/order.html', context)
    else:
        return render(request, 'meduser/home.html')
