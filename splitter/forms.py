from django.forms import forms, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Bill


class BillCreateForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('title',)
        labels = {
            'title': _('Name'),
        }
        help_texts = {
            'title': _('The current date and time will be used if name field is empty.'),
        }
        error_messages = {
            'title': {
                'max_length': _("Name is too long."),
            },
        }


class BillUpdateForm(ModelForm):

    class Meta:
        model = Bill
        fields = ('title', 'tax', 'tip',)
        labels = {
            'title': _('Name'),
        }


class BillUpdateTaxPercentForm(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     initial = kwargs.get('initial', {})
    #     initial['tax'] = 0
    #     kwargs['initial'] = initial
    #     super(BillUpdateTaxPercentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bill
        fields = ('tax_percent',)
        help_texts = {
            'tax_percent': _('Please enter a percent(%) amount.')
        }


class BillUpdateTaxAmountForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('tax',)
        help_texts = {
            'tax': _('Please enter a currency amount.')
        }


class BillUpdateTipForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('tip',)
        labels = _('Tax/Service Charge')
        help_texts = {
            'tip': _('Please enter currency amount.')
        }