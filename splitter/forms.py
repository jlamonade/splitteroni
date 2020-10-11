from django.forms import forms, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Bill


class BillCreateForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('title', 'tax', 'tip',)
        labels = {
            'title': _('Name'),
        }
        help_texts = {
            'title': _('The current date and time will be used if no name is provided'),
            'tax': _('Please enter a currency amount. You can adjust this later.'),
            'tip': _('Please enter a currency amount. You can adjust this later.'),
        }
        error_messages = {
            'title': {
                'max_length': _("Name is too long."),
            },
            'tax': {
                'max_digits': _("Amount is too large."),
            },
            'title': {
                'max_digits': _("Amount is too large."),
            },
        }

<<<<<<< HEAD

class BillUpdateForm(BillCreateForm):
    class Meta:
        model = Bill
        fields = ('tax', 'tip',)
        help_texts = {
            'tax': _('Please enter a currency amount.'),
            'tip': _('Please enter a currency amount.'),
        }
=======
# class BillUpdateForm(ModelForm):
#     class Meta:
#         model = Bill
#         fields = ('tax', 'tip',)

>>>>>>> origin/logicFix

