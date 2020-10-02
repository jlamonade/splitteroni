from django.shortcuts import render
from django.views.generic import CreateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = Person.objects.filter(
            bill=get_object_or_404(Bill, id=self.kwargs['pk']))
        return context


class PersonCreateView(CreateView):
    model = Person
    template_name = 'splitter/person_create.html'
    fields = ('name',)

    def form_valid(self, form):
        self.bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = self.bill
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.bill.id])


class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'splitter/person_delete.html'

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.object.bill.id])