from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import datetime

# Create your models here.
class Bill(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tip = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0)
    tax = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=0)

    def __str__(self):
        if not self.title:
            return self.date_created.strftime("%m/%d/%y %I:%M%p")
        else:
            return self.title.title()

    def get_order_total(self):
        total = 0
        for item in Item.objects.filter(bill=self):
            total += item.price
        return total

    @property
    def get_shared_items_total(self):
        total = 0
        for item in Item.objects.filter(shared=True, bill=self):
            total += item.price
        return total

    def get_absolute_url(self):
        return reverse('bill-detail', args=[self.id])


class Person(models.Model):
    name = models.CharField(max_length=20)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.name

    def get_person_total(self):
        total = 0
        for item in Item.objects.filter(person=self):
            total += item.price
        return total


class Item(models.Model):
    title = models.CharField(max_length=50)
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







