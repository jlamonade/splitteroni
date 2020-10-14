class BillUpdateViewMixin(object):

    def form_valid(self, form):
        bill = get_object_or_404(Bill, id=self.kwargs['pk'])
        form.instance.bill = bill
        return super().form_valid(form)