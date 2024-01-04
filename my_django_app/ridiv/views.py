from django.shortcuts import render,redirect
from django.views import View
from rest_framework import generics #Import generic class-based views from the Django Rest Framework.
from .forms import InvoiceForm, InvoiceDetailForm,UpdateInvoiceDetailForm,DeleteInvoiceForm
from .models import Invoice, InvoiceDetail
from .serialiser import InvoiceSerializer, InvoiceDetailSerializer
from django.http import HttpResponse
from django.urls import reverse


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer

#fetch all records in invoice & invoice-details
class InvoiceListView(View):
    
    template_name = 'C:/Users/DELL/Documents/my_django_app/my_django_app/ridiv/templates/all_items.html'
    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        details=InvoiceDetail.objects.all()
        return render(request, self.template_name, {'invoices': invoices,'details':details})

#fetch all details wrt invoice-id
class GetInvoiceDetailsView(View):
    template_name = 'C:/Users/DELL/Documents/my_django_app/my_django_app/ridiv/templates/all_items.html'
    result_template_name = 'C:/Users/DELL/Documents/my_django_app/my_django_app/ridiv/templates/result.html'
    def post(self, request, *args, **kwargs):
        invoice_id = request.POST.get('invoice_id')
        try:
            invoice = Invoice.objects.get(pk=invoice_id)
            details = invoice.details.all()
            print(invoice,details)
            return render(request, self.result_template_name, {'invoice': invoice, 'details': details})
        except Invoice.DoesNotExist:
            return HttpResponse("Invoice ID doesn't exist", status=400)
            
#to insert a new-invoice
class CreateInvoiceView(View):
    template_name = 'C:/Users/DELL/Documents/my_django_app/my_django_app/ridiv/templates/create_invoice.html'

    def get(self, request, *args, **kwargs):
        invoice_form = InvoiceForm()
        detail_form = InvoiceDetailForm()
        return render(request, self.template_name, {'invoice_form': invoice_form, 'detail_form': detail_form})

    def post(self, request, *args, **kwargs):
        invoice_form = InvoiceForm(request.POST)
        detail_form = InvoiceDetailForm(request.POST)

        if invoice_form.is_valid() and detail_form.is_valid():
            # Save the Invoice
            invoice = invoice_form.save()

            # Save the InvoiceDetail with the associated Invoice
            detail = detail_form.save(commit=False)
            detail.invoice = invoice
            detail.save()

            return redirect('get_all_items')  # Redirect to the invoice list view or any other view as needed

        return render(request, self.template_name, {'invoice_form': invoice_form, 'detail_form': detail_form})

#update invoice
class UpdateInvoiceDetailView(View):
    template_name = 'C:/Users/DELL/Documents/my_django_app/my_django_app/ridiv/templates/update_invoice_detail.html'

    def get(self, request, *args, **kwargs):
        form = UpdateInvoiceDetailForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UpdateInvoiceDetailForm(request.POST)

        if form.is_valid():
            invoice_id = form.cleaned_data['invoice_id']
            quantity = form.cleaned_data['quantity']

            try:
                invoice = Invoice.objects.get(pk=invoice_id)
                detail = invoice.details.first()  # Assuming there is only one detail for each invoice-id

                if detail:
                    # Update the quantity and recalculate the total price
                    detail.quantity = quantity
                    detail.price = detail.unit_price * quantity
                    detail.save()

                    return redirect('get_all_items')  # Redirect to the invoice list view
            except Invoice.DoesNotExist:
                return HttpResponse("Invoice ID doesn't exist", status=400)

        return render(request, self.template_name, {'form': form})
    
#delete invoice based on invoice-id
class DeleteInvoiceView(View):
    template_name = 'C:/Users/DELL/Documents/my_django_app/my_django_app/ridiv/templates/delete_invoice.html'

    def get(self, request, *args, **kwargs):
        form = DeleteInvoiceForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DeleteInvoiceForm(request.POST)

        if form.is_valid():
            invoice_id = form.cleaned_data['invoice_id']

            try:
                invoice = Invoice.objects.get(pk=invoice_id)
                invoice.delete()

                return redirect('get_all_items')  # Redirect to the invoice list view
            except Invoice.DoesNotExist:
                return HttpResponse("Invoice ID doesn't exist", status=400)


        return render(request, self.template_name, {'form': form})