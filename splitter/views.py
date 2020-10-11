from django.views.generic import CreateView, DetailView, DeleteView, ListView, UpdateView, FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bill, Person, Item
<<<<<<< HEAD
from .forms import BillCreateForm, BillUpdateForm
=======
from .forms import BillCreateForm#, BillUpdateForm
>>>>>>> origin/logicFix


# Create your views here.
class BillCreateView(CreateView):
    template_name = 'splitter/bill_create.html'
    form_class = BillCreateForm

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
        context['people'] = Person.objects.filter(
            bill=self.object.id)
        context['shared_items'] = Item.objects.filter(bill=self.object.id, shared=True)
        return context


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
        qs = Bill.objects.filter(owner=self.request.user)
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
    fields = ('tax', 'tip',)
    template_name = 'splitter/bill_update.html'
<<<<<<< HEAD
    form_class = BillUpdateForm
=======
>>>>>>> origin/logicFix

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        return super().form_valid(form)

