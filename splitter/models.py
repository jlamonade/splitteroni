import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal

from .utils import _check_tip_tax_then_add


# Create your models here.
class Bill(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tip = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    tax_percent = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index'),
        ]

    def __str__(self):
        if not self.title:
            return self.date_created.strftime("%m/%d/%y %I:%M%p")
        else:
            return self.title.title()

    def get_tax_amount(self):
        total = self.get_order_subtotal()
        if self.tax_percent:
            tax_amount = total * (self.tax_percent / 100)
            bill = Bill.objects.get(id=self.id)
            bill.tax = tax_amount
            bill.save()
            return Decimal(tax_amount).quantize(Decimal('.01'))
        elif self.tax:
            return Decimal(self.tax).quantize(Decimal('.01'))

    def get_order_grand_total(self):
        # Returns the sum of all items including tax and tip
        total = _check_tip_tax_then_add(self) + self.get_order_subtotal()
        return Decimal(total)

    def get_order_subtotal(self):
        total = 0
        items = Item.objects.filter(bill=self)
        for item in items:
            total += Decimal(item.price)
        return Decimal(total)

    def get_shared_items_total(self):
        # Returns sum of shared items only
        total = 0
        items = Item.objects.filter(shared=True, bill=self)
        for item in items:
            total += Decimal(item.price)
        return Decimal(total)

    def get_absolute_url(self):
        return reverse('bill-detail', args=[self.id])


class Person(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=30)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='people')

    class Meta:
        verbose_name_plural = 'people'
        indexes = [
            models.Index(fields=['id'], name='person_id_index'),
        ]

    def __str__(self):
        return self.name.title()

    def get_shared_items_split(self):
        # Returns the amount every person owes inside the shared items including tax and tip
        total = _check_tip_tax_then_add(self.bill)
        person_count = self.bill.people.all().count()
        items = self.bill.items.filter(shared=True)
        for item in items:
            total += Decimal(item.price)
        split_amount = Decimal(total / person_count)
        return Decimal(split_amount)

    def get_person_total(self):
        # Returns the sum of the person's items and their share of the shared items total
        total = 0
        items = Item.objects.filter(person=self)
        for item in items:
            total += Decimal(item.price)
        return Decimal(total + self.get_shared_items_split()).quantize(Decimal('.01'))

    def get_absolute_url(self):
        return reverse('bill-detail', args=[self.bill.id])


class Item(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='items',
        blank=True,
        null=True
    )
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    shared = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='item_id_index'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bill-detail', args=[self.bill.id])
