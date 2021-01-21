from django.contrib import admin

# Register your models here.
from lend_and_returns.models import LendOrder, LendLine, InvoiceLine, Invoice

class LendInline(admin.StackedInline):
    model = LendLine

class LendAdmin(admin.ModelAdmin):
    inlines = (LendInline,)

class InvoiceInline(admin.StackedInline):
    model = InvoiceLine

class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceInline,)

admin.site.register(LendOrder, LendAdmin)
admin.site.register(Invoice, InvoiceAdmin)