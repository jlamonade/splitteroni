from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Bill, Person, Item

# Create your tests here.
class SplitterTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testpass',
        )
        self.bill = Bill.objects.create(
            title='testbill',
            tip=12.00,
            tax=13.00,
            owner=self.user,
        )
        self.person = Person.objects.create(
            name='testperson',
            bill=self.bill
        )
        self.item = Item.objects.create(
            title='testitem',
            price=14.00,
            person=self.person,
            bill=self.bill,
        )
        self.shared_item = Item.objects.create(
            title='testshareditem',
            price=15.00,
            bill=self.bill,
            shared=True,
        )
        # Testing tax percent/amount
        self.bill_two = Bill.objects.create(
            title='testbill2',
            tip_percent=15,
            tax_percent=8.875,
            owner=self.user,
        )
        self.item_two = Item.objects.create(
            title='testitem2',
            price=14.00,
            bill=self.bill_two,
            shared=True,
        )
        self.bill_total = self.item.price + self.shared_item.price + self.bill.tax + self.bill.tip
        self.shared_item_total = self.bill.tip + self.bill.tax + self.shared_item.price
        self.bill_detail_response = self.client.get(self.bill.get_absolute_url())
        self.bill_two_response = self.client.get(self.bill_two.get_absolute_url())

    def test_bill_object(self):
        self.assertEqual(self.bill.title, 'testbill')
        self.assertEqual(self.bill.tip, 12.00)
        self.assertEqual(self.bill.tax, 13.00)
        self.assertEqual(self.bill.owner, self.user)

    def test_bill_list_view_for_logged_in_user(self):
        self.client.login(email='testuser@email.com', password='testpass')
        response = self.client.get(reverse('bill-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testbill'.title())
        self.assertTemplateUsed(response, 'splitter/bill_list.html')

    def test_bill_list_view_for_logged_out_users(self):
        response = self.client.get(reverse('bill-list'))
        self.assertEqual(response.status_code, 302)

    def test_bill_detail_view(self):
        no_response = self.client.get('/bill/12345/')
        self.assertEqual(self.bill_detail_response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(self.bill_detail_response, 'testbill'.title())
        self.assertContains(self.bill_detail_response, '12.00')
        self.assertContains(self.bill_detail_response, '13.00')
        self.assertContains(self.bill_detail_response, self.item.price)
        self.assertContains(self.bill_detail_response, self.shared_item.price)
        self.assertContains(self.bill_detail_response, self.bill_total)
        self.assertTemplateUsed(self.bill_detail_response, 'splitter/bill_detail.html')

    def test_person_object(self):
        self.assertEqual(self.person.name, 'testperson')
        self.assertEqual(self.person.bill, self.bill)

    def test_person_object_in_bill_detail_view(self):
        self.assertContains(self.bill_detail_response, 'testperson'.title())

    def test_item_object(self):
        self.assertEqual(self.item.title, 'testitem')
        self.assertEqual(self.item.price, 14.00)
        self.assertEqual(self.item.bill, self.bill)
        self.assertEqual(self.item.person, self.person)

    def test_item_object_in_bill_detail_view(self):
        self.assertContains(self.bill_detail_response, 'testitem')
        self.assertContains(self.bill_detail_response, 14.00)

    def test_shared_item_object(self):
        self.assertEqual(self.shared_item.title, 'testshareditem')
        self.assertEqual(self.shared_item.price, 15.00)
        self.assertEqual(self.shared_item.bill, self.bill)

    def test_shared_item_object_in_bill_detail_view(self):
        self.assertContains(self.bill_detail_response, 'testshareditem')
        self.assertContains(self.bill_detail_response, 15.00)

    def test_bill_model_methods(self):
        """Tests for Bill model methods."""

        # Bill.get_order_total()
        self.assertEqual(self.bill.get_order_grand_total(), self.bill_total)

        # Bill.get_shared_items_total()
        self.assertEqual(self.bill.get_shared_items_total(), self.shared_item.price)

    def test_person_model_methods(self):
        """Tests for Person model methods."""

        # Person.get_shared_items_split()
        self.assertEqual(self.person.get_shared_items_split(), self.shared_item_total)

        # Person.get_person_total()
        self.assertEqual(self.person.get_person_total(), self.bill.get_order_grand_total())

    def test_bill_calculate_tax(self):
        self.assertContains(self.bill_two_response, Decimal(self.bill_two.get_tax_amount()))
        self.assertContains(self.bill_two_response, self.bill_two.tax_percent)
        self.bill_two.tax = 12.00
        self.assertContains(self.bill_two_response, Decimal(self.bill_two.tax))

    def test_bill_calculate_tip(self):
        self.assertContains(self.bill_two_response, Decimal(self.bill_two.get_tip_amount()))
        self.assertContains(self.bill_two_response, self.bill_two.tip_percent)
        self.bill_two.tip = 12.00
        self.assertContains(self.bill_two_response, Decimal(self.bill_two.tip))
