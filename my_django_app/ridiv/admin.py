from django.contrib import admin

# invoices/admin.py
from django.contrib import admin
from .models import Invoice, InvoiceDetail

admin.site.register(Invoice)
admin.site.register(InvoiceDetail)

