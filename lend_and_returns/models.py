from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from meduser.models import Company, Currency, Products


def increment_order_number():
    last_order = LendOrder.objects.all().order_by('id').last()
    if not last_order:
         return 'LEND0001'
    order_no = last_order.name
    order_int = int(order_no.split('LEND')[-1])
    new_order_int = str(order_int + 1)
    new_order_int = new_order_int.zfill(4)
    new_order_no = 'LEND' + str(new_order_int)
    return new_order_no

def setCompany():
    return Company.objects.all()[0]

def setCurrency():
    company = Company.objects.all()[0]
    return company.currency

class LendOrder(models.Model):
    STATUS = (
        ('pending', 'Pending for return'),
        ('pending_approval', 'Requested return'),
        ('returned', 'Returned'),
        ('cancel', 'Cancelled'),
    )
    name = models.CharField(max_length=100, default=increment_order_number, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    edited_date = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    returned_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    total_received = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    amount_to_refund = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    complete = models.BooleanField(null=True, blank=True)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, default=setCompany, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, null=True, default=setCurrency, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Lend'

class LendLine(models.Model):
    STATUS = (
        ('pending', 'Pending for return'),
        ('pending_approval', 'Requested return'),
        ('returned', 'Returned'),
        ('cancel', 'Cancelled'),
    )
    lend = models.ForeignKey(LendOrder,related_name="lendline", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    expected_return_date = models.DateField(null=True,blank=True)
    returned_date = models.DateField(null=True, blank=True)
    edited_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    line_total = models.DecimalField(max_digits=5,decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    company = models.ForeignKey(Company, null=True, default=setCompany, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, null=True, default=setCurrency, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.lend)}_{str(self.product)}'

    class Meta:
        verbose_name_plural = 'Lend lines'


def increment_invoice_number():
    last_invoice = Invoice.objects.all().order_by('id').last()
    if not last_invoice:
         return 'INV0001'
    invoice_no = last_invoice.name
    invoice_int = int(invoice_no.split('INV')[-1])
    new_invoice_int = str(invoice_int + 1)
    new_invoice_int = new_invoice_int.zfill(4)
    new_invoice_no = 'INV' + str(new_invoice_int)
    return new_invoice_no


class Invoice(models.Model):
    TYPE = (
        ('in', 'In'),
        ('out', 'Out'),
    )

    name = models.CharField(max_length=100, default=increment_invoice_number, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    lend_order = models.ForeignKey(LendOrder, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    total_received = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, default=setCompany, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, null=True, default=setCurrency, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.name)}_{str(self.lend_order)}_{str(self.type)}'

    class Meta:
        verbose_name_plural = 'Invoices'

class InvoiceLine(models.Model):
    TYPE = (
        ('in', 'In'),
        ('out', 'Out'),
    )

    lend = models.ForeignKey(LendOrder, on_delete=models.CASCADE)
    lend_line = models.ForeignKey(LendLine, on_delete=models.CASCADE)
    user_line = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    edited_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    line_total = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE,default='in')
    company = models.ForeignKey(Company, null=True, default=setCompany, blank=True, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, null=True, default=setCurrency, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(str(self.type) + '_'+ str(self.lend) + '_'+ str(self.product))

    class Meta:
        verbose_name_plural = 'Invoice lines'

    def delete(self, *args, **kwargs):
        super(InvoiceLine, self).delete(*args, **kwargs)
        lines = InvoiceLine.objects.filter(invoice=self.invoice)
        total = 0
        for line in lines:
            total += line.line_total
        self.invoice.total = total
        self.invoice.save()

    def save(self, *args, **kwargs):
        super(InvoiceLine, self).save(*args, **kwargs)
        lines = InvoiceLine.objects.filter(invoice=self.invoice)
        total = 0
        for line in lines:
            total += line.line_total
        self.invoice.total = total
        self.invoice.save()