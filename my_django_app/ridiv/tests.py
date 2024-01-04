
from django.test import TestCase
from django.urls import reverse
from .models import Invoice,InvoiceDetail

#testcase for listing all data in invoices table
class InvoiceListViewTest(TestCase):
    def setUp(self):
        # Create test data for invoices
        self.invoice1 = Invoice.objects.create(date='2024-01-01', customer_name='cus1')

    def test_invoice_list_view(self):
        # Issue a GET request to the view
        response = self.client.get(reverse('get_all_items'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the rendered context contains the invoices
        self.assertQuerysetEqual(
            response.context['invoices'],
            ['Invoice 1 - cus1'],
            transform=str
        )
        # Check if the rendered HTML contains the expected data
        self.assertContains(response, 'cus1')

#testcase for geeting invoice & invoice details based on invoice-id
class GetInvoiceDetailsViewTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(date='2022-01-01', customer_name='Test Customer')
        self.detail1 = InvoiceDetail.objects.create(invoice=self.invoice, description='maggie', quantity=2, unit_price=10, price=20)
        
    def test_get_invoice_details_view(self):
        url = reverse('get-invoice-details')
        data = {'invoice_id': self.invoice.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Customer')
        self.assertContains(response, 'maggie')
        
#testcase for inserting new record in invoice & invoice-details
class CreateInvoiceViewTest(TestCase):
    def test_create_invoice_and_verify_in_list(self):
        # Access the create-invoice page
        create_invoice_url = reverse('create-invoice')
        response_create = self.client.get(create_invoice_url)
        self.assertEqual(response_create.status_code, 200)

        #  creating a new invoice
        response_save = self.client.post(create_invoice_url, {
            'date': '2022-01-01',
            'customer_name': 'Test Customer',
            'description': 'Test Item',
            'quantity': 2,
            'unit_price': 10,
            'price': 20,
        })

        # Verify that the save redirects to the invoice-list
        self.assertEqual(response_save.status_code, 302)
        self.assertRedirects(response_save, reverse('get_all_items'))

        # Verify that the newly created invoice appears in the list
        response_list = self.client.get(reverse('get_all_items'))
        self.assertContains(response_list, 'Test Customer')
        self.assertContains(response_list, 'Test Item')

#testcase for updating invoice-details
class UpdateInvoiceDetailViewTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(date='2022-01-01', customer_name='Test Customer')
        self.detail = InvoiceDetail.objects.create(invoice=self.invoice, description='Test Item', quantity=3, unit_price=10, price=20)

    def test_update_invoice_detail_and_verify_in_list(self):
        # Access the update-invoice-detail page
        update_detail_url = reverse('update-invoice-detail')
        response_update = self.client.get(update_detail_url)
        self.assertEqual(response_update.status_code, 200)

        # Simulate updating the invoice detail
        response_save = self.client.post(update_detail_url, {
            'invoice_id': self.invoice.id,
            'quantity': 3,
        })

        self.assertRedirects(response_save, reverse('get_all_items'))
        
        response_list = self.client.get(reverse('get_all_items'))
        print(response_list)
        self.assertContains(response_list, 50)
        
        self.detail.refresh_from_db()
        # Verify that the total price is correctly calculated
        self.assertEqual(self.detail.price, self.detail.unit_price * 3)

#testcase for deleting a record based on invoice-id
class DeleteInvoiceViewTest(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(date='2022-01-01', customer_name='Test Customer')
        self.detail = InvoiceDetail.objects.create(invoice=self.invoice, description='Test Item', quantity=1, unit_price=10, price=10)

    def test_delete_invoice_and_verify_in_list(self):
        # Access the delete-invoice page
        delete_invoice_url = reverse('delete-invoice')
        response_delete = self.client.get(delete_invoice_url)
        self.assertEqual(response_delete.status_code, 200)

        # Simulate deleting the invoice
        response_save = self.client.post(delete_invoice_url, {
            'invoice_id': self.invoice.id,
        })

        # Verify that the save redirects to the invoice-list
        self.assertEqual(response_save.status_code, 302)
        self.assertRedirects(response_save, reverse('get_all_items'))

        # Verify that the deleted invoice doesn't appear in the list
        response_list = self.client.get(reverse('get_all_items'))
        self.assertNotContains(response_list, 'Test Customer')
        self.assertNotContains(response_list, 'Test Item')