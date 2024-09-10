from django import forms
from .models import WiFiPlan

from .validator import validate_kenya_phone_number

class WiFiPlanForm(forms.ModelForm):
    class Meta:
        model = WiFiPlan
        fields = ['name', 'speed', 'price', 'description']



class PaymentForm(forms.Form):
    amount = forms.IntegerField()
    phone_number = forms.CharField(
        max_length=13,
        label='Phone Number',
        validators=[validate_kenya_phone_number],
        initial='+254',
        help_text='Enter your phone number starting with +254'
    )


\

