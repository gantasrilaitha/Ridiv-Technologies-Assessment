# forms.py
from django import forms
from .models import Invoice, InvoiceDetail

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['date', 'customer_name']

class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'unit_price', 'price']
class UpdateInvoiceDetailForm(forms.Form):
    invoice_id = forms.IntegerField()
    quantity = forms.IntegerField()
class DeleteInvoiceForm(forms.Form):
    invoice_id = forms.IntegerField()