from django.contrib import admin

# Register your models here.
from .models import Landlord, RentalProperty, Contract
admin.site.register(Landlord)
admin.site.register(RentalProperty)
admin.site.register(Contract)