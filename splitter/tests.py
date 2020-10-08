from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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
            tip='12.00',
            tax='13.00',
            owner=self.user,
        )
        self.person = Person.objects.create(
            name='testperson',
            bill=self.bill
        )
        self.item = Item.objects.create(
            title='testitem',
            price='14.00',
            person=self.person,
            bill=self.bill
        )
        self.shared_item = Item.objects.create(
            title='testshareditem',
            price='15.00',
            person=self.person,
            bill=self.bill
        )

    def test_bill_object(self):
        self.assertEqual(self.bill.title, 'testbill')
        self.assertEqual(f'{self.bill.tip}', '12.00')
        self.assertEqual(f'{self.bill.tax}', '13.00')
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
        response = self.client.get(self.bill.get_absolute_url())
        no_response = self.client.get('/bill/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'testbill'.title())
        self.assertContains(response, '12.00')
        self.assertContains(response, '13.00')
        self.assertTemplateUsed(response, 'splitter/bill_detail.html')

    def test_person_object(self):
        self.assertEqual(self.person.name, 'testperson')
        self.assertEqual(self.person.bill, self.bill)

    def test_person_object_in_bill_detail_view(self):
        response = self.client.get(self.bill.get_absolute_url())
        self.assertContains(response, 'testperson'.title())

    def test_item_object(self):
        self.assertEqual(self.item.title, 'testitem')
        self.assertEqual(f'{self.item.price}', '14.00')
        self.assertEqual(self.item.bill, self.bill)
        self.assertEqual(self.item.person, self.person)

    def test_item_object_in_bill_detail_view(self):
        response = self.client.get(self.bill.get_absolute_url())
        self.assertContains(response, 'testitem')
        self.assertContains(response, '14.00')

    def test_shared_item_object(self):
        self.assertEqual(self.shared_item.title, 'testshareditem')
        self.assertEqual(f'{self.shared_item.price}', '15.00')
        self.assertEqual(self.shared_item.bill, self.bill)
        self.assertEqual(self.shared_item.person, self.person)

    def test_shared_item_object_in_bill_detail_view(self):
        response = self.client.get(self.bill.get_absolute_url())
        self.assertContains(response, 'testshareditem')
        self.assertContains(response, '15.00')

