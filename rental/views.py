import os
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic 
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse

from django.forms.models import construct_instance
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
    user = UserModel.objects.first()
    if request.method == 'POST':
        form = NewRentalPropertyForm(request.POST, request.FILES)
        #contract_form = NewContractForm(request.POST, prefix = "contracts")
        if form.is_valid():
            print ("all validation passed")
            rentalproperty = form.save()
            #contract_form.cleaned_data["rentalproperty"] = rentalproperty
            #contract.rentalproperty = rentalproperty
            #contract = contract_form.save()
            return HttpResponseRedirect(reverse("rental:new_contract"))
        else:
            messages.error(request, "Error")
            
    else: 
        form = NewRentalPropertyForm()
        #contract_form = NewContractForm(prefix = "contracts")
    return render(request, 'rental/new_rental.html', {
        'rentalproperty': rentalproperty,
        'form': form,
        #'contract_form': contract_form,
        })

def new_contract(request, pk):
    rentalproperty = get_object_or_404(RentalProperty, pk=pk)
    if request.method == 'POST':
        form = NewContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.rentalproperty = rentalproperty
            contract.save()
            return HttpResponseRedirect(reverse("rental:home"))
        else:
            messages.error(request, "Error")
            
    else:
        form = NewContractForm()
    return render(request, 'rental/new_contract.html', {
        'rentalproperty': rentalproperty,
        'form': form,
        })

class UpdateView(generic.UpdateView):
    model = RentalProperty
    form_class = NewRentalPropertyForm
    template_name = 'new_rental.html'
    success_url = reverse_lazy('rental:home')

class DeleteView(generic.DeleteView):
    model = RentalProperty
    success_url = reverse_lazy('rental:home')