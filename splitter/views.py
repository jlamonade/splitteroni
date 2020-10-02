from django.shortcuts import render
from django.views.generic import CreateView, DetailView

from .models import Bill, Person, Item


# Create your views here.
class BillCreateView(CreateView):
    model = Bill
    template_name = 'splitter/bill_create.html'
    fields = ('title',)


class BillDetailView(DetailView):
    model = Bill
    template_name = 'splitter/bill_detail.html'
    context_object_name = 'bill'