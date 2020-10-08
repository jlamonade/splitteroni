import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


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
    tip = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0)
    tax = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        if not self.title:
            return self.date_created.strftime("%m/%d/%y %I:%M%p")
        else:
            return self.title.title()

    def get_order_total(self):
        total = self.tip + self.tax
        for item in Item.objects.filter(bill=self):
            total += item.price
        return total

    def get_shared_items_total(self):
        total = 0
        for item in Item.objects.filter(shared=True, bill=self):
            total += item.price
        return total

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

    def __str__(self):
        return self.name.title()

    def get_shared_items_split(self):
        total = self.bill.tax + self.bill.tip
        person_count = self.bill.people.all().count()
        for item in self.bill.items.filter(shared=True):
            total += item.price
        split_amount = total / person_count
        return round(split_amount, 2)

    def get_person_total(self):
        total = 0
        for item in Item.objects.filter(person=self):
            total += item.price
        return total + self.get_shared_items_split()

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bill-detail', args=[self.bill.id])







