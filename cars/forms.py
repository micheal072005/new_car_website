from django import forms
from .models import *



# Form for the contact form
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]



# This form is used to collect payment information from the user.
class PurchaseForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    transaction_id = forms.CharField(max_length=100)
    proof_of_payment = forms.ImageField(required=True)


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Brand.objects.filter(name=name).exists():
            raise forms.ValidationError('This brand name already exists.')
        return name
