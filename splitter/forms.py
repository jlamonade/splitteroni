from django.forms import forms, ModelForm

from .models import Bill


class BillCreateForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('title', 'tax', 'tip',)
