from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView, FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from decimal import Decimal

from .models import Bill, Person, Item
from .forms import (BillCreateForm,
                    BillUpdateForm,
                    BillUpdateTaxPercentForm,
                    BillUpdateTaxAmountForm,
                    BillUpdateTipForm,
                    BillUpdateTipPercentForm)
from .mixins import BillUpdateViewMixin


# Create your views here.
class BillCreateView(CreateView):
    template_name = 'splitter/bill_create.html'
    form_class = BillCreateForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
            return super().form_valid(form)
        else:
            self.request.session.create()
            form.instance.session = self.request.session.session_key
            return super().form_valid(form)


class BillDetailView(DetailView):
    model = Bill
    template_name = 'splitter/bill_detail.html'
    context_object_name = 'bill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = Person.objects.filter(
            bill=self.object.id)
        context['shared_items'] = Item.objects.filter(bill=self.object.id, shared=True)
        if self.object.tax_percent:
            context['tax_percentage'] = Decimal(self.object.tax_percent).quantize(Decimal('0.001'))
        if self.object.tip_percent:
            context['tip_percentage'] = Decimal(self.object.tip_percent.quantize(Decimal('0')))
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Bill, id=pk)
        if self.request.user.is_authenticated:
            return obj
        elif self.request.session.session_key == obj.session:
            return obj
        else:
            return Http404


class PersonCreateView(CreateView):
    model = Person
    template_name = 'splitter/person_create.html'
    fields = ('name',)

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        return super().form_valid(form)


class BillDeleteView(DeleteView):
    model = Bill
    template_name = 'splitter/bill_delete.html'

    def get_success_url(self):
        return reverse_lazy('bill-list')


class BillListView(LoginRequiredMixin ,ListView):
    template_name = 'splitter/bill_list.html'
    context_object_name = 'bills'
    login_url = 'account_login'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Bill.objects.filter(owner=self.request.user).order_by('-date_created')
        elif not self.request.user.is_authenticated:
            qs = Bill.objects.filter(session=self.request.session.session_key).order_by('-date_created')
        return qs


class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'splitter/person_delete.html'

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.object.bill.id])


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


class SharedItemCreateView(CreateView):
    model = Item
    template_name = "splitter/item_create.html"
    fields = ('title', 'price',)

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['bill_id'])
        form.instance.bill = bill
        form.instance.shared = True
        return super().form_valid(form)


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'splitter/item_delete.html'

    def get_success_url(self):
        return reverse_lazy('bill-detail', args=[self.object.bill.id])


class BillUpdateView(UpdateView):
    model = Bill
    template_name = 'splitter/bill_update.html'
    form_class = BillUpdateForm

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        return super().form_valid(form)


class BillUpdateTaxPercentView(UpdateView):
    model = Bill
    form_class = BillUpdateTaxPercentForm
    template_name = 'splitter/bill_update_tax_percent.html'

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        form.instance.tax = None
        return super().form_valid(form)


class BillUpdateTaxAmountView(UpdateView):
    model = Bill
    form_class = BillUpdateTaxAmountForm
    template_name = 'splitter/bill_update_tax_amount.html'

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        form.instance.tax_percent = None
        return super().form_valid(form)


class BillUpdateTipAmountView(UpdateView):
    model = Bill
    form_class = BillUpdateTipForm
    template_name = 'splitter/bill_update_tip.html'

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        form.instance.tip_percent = None
        return super().form_valid(form)


class BillUpdateTipPercentView(UpdateView):
    model = Bill
    form_class = BillUpdateTipPercentForm
    template_name = 'splitter/bill_update_tip_percent.html'

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        form.instance.tip = None
        return super().form_valid(form)
