from django import forms

from .models import BillingData

class BillingDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = BillingData
        fields = '__all__'

