from django.contrib import admin
from .models import Bill, Person, Item

# Register your models here.
admin.site.register(Bill)
admin.site.register(Person)
admin.site.register(Item)
