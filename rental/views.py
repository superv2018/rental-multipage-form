from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic 
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
# Create your views here.
from .models import Landlord, RentalProperty, Contract
from .forms import NewRentalPropertyForm, NewContractForm

UserModel = get_user_model()

class HomeView(generic.ListView):
    model = RentalProperty
    template_name = 'rental/index.html'

    #def get_queryset(self):
        #query = super().get_queryset()
        #return Landlord.objects.filter(rentalproperty__created_by=self.request.user)

class DetailView(generic.DetailView):
    model = RentalProperty
    template_name = 'rental/detail.html'
    context_object_name = 'property'

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['landlord']= Landlord.objects.all()
        #context['contract']= Contract.objects.all()
        #return context

  
def new_rental(request, pk):
    rentalproperty = get_object_or_404(RentalProperty, pk=pk)
    #user = UserModel.objects.first()
    if request.method == 'POST':
        rental_form = NewRentalPropertyForm(request.POST, request.FILES, prefix = "rentals")
        contract_form = NewContractForm(request.POST, prefix = "contracts")
        if rental_form.is_valid() and contract_form.is_valid():
            print ("all validation passed")
            rentalproperty = rental_form.save()
            contract_form.cleaned_data["rentalproperty"] = rentalproperty
            print(contract_form)
            contract = contract_form.save(commit=False)
            contract.rentalproperty = rentalproperty
            contract = contract_form.save()
            return HttpResponseRedirect(reverse("rental:home"))
        else:
            messages.error(request, "Error")
            contract = Contract.objects.get(pk=pk)
           
    else: 
        rental_form = NewRentalPropertyForm(prefix = "rentals")
        contract_form = NewContractForm(prefix = "contracts")
        contract = Contract.objects.get(pk=pk)
    return render(request, 'rental/new_rental.html', {
        #'rentalproperty': rentalproperty,
    'rental_form': rental_form,
    'contract_form': contract_form,
    'contract': contract,
        
    })

    


class UpdateView(generic.UpdateView):
    model = RentalProperty
    form_class = NewRentalPropertyForm
    template_name = 'new_rental.html'
    success_url = reverse_lazy('rental:home')

class DeleteView(generic.DeleteView):
    model = RentalProperty
    success_url = reverse_lazy('rental:home')