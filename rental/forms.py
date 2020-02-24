from django import forms
from .models import Landlord, RentalProperty, Contract

class NewLandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ['address']


class NewRentalPropertyForm(forms.ModelForm):
    class Meta:
        model = RentalProperty
        fields = ['landlord','created_by','title','type_of_property_listing', 'street', 'borough', 'image']

class NewContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['rentalproperty','insurance_required', 'other_terms']