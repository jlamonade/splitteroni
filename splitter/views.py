from django.shortcuts import render
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import Bill, Person, Item


# Create your views here.
class BillCreateView(CreateView):
    model = Bill
    template_name = 'splitter/bill_create.html'
    fields = ('title',)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
            return super().form_valid(form)
        else:
            return super().form_valid(form)


class BillDetailView(DetailView):
    model = Bill
    template_name = 'splitter/bill_detail.html'
    context_object_name = 'bill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        context['people'] = Person.objects.filter(
            bill=bill)
        return context


class PersonCreateView(CreateView):
    model = Person
    template_name = 'splitter/person_create.html'
    fields = ('name',)

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.bill.id])


class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'splitter/person_delete.html'

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.object.bill.id])


class BillListView(ListView):
    template_name = 'splitter/bill_list.html'
    context_object_name = 'bills'

    def get_queryset(self):
        qs = Bill.objects.filter(owner=self.request.user)
        return qs


class ItemCreateView(CreateView):
    model = Item
    template_name = 'splitter/item_create.html'
    fields = ('title', 'price',)

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['bill_id'])
        person = get_object_or_404(Person, id=self.kwargs['person_id'])
        form.instance.bill = bill
        form.instance.person = person
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.object.bill.id])

