# invoices/urls.py
from django.urls import path
from .views import InvoiceListCreateView, InvoiceDetailView, GetInvoiceDetailsView,CreateInvoiceView
from .views import InvoiceListView,UpdateInvoiceDetailView,DeleteInvoiceView
urlpatterns = [
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoice/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice-list/', InvoiceListView.as_view(), name='get_all_items'),
    path('get-invoice-details/', GetInvoiceDetailsView.as_view(), name='get-invoice-details'),
    path('create-invoice/', CreateInvoiceView.as_view(), name='create-invoice'),
    path('update-invoice-detail/', UpdateInvoiceDetailView.as_view(), name='update-invoice-detail'),
    path('delete-invoice/', DeleteInvoiceView.as_view(), name='delete-invoice'),
]
#The as_view() method converts the class-based view into a function-based view.
#name provides a unique identifier for this URL.