from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from PIL import Image
# Create your models here.

UserModel = get_user_model()

class Landlord(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.address)


class RentalProperty(models.Model):
    landlord = models.ForeignKey("Landlord", related_name='rentalpropertys', on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserModel, related_name='rentalpropertys', on_delete=models.CASCADE)
    title = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    PROPERTY_LISTING_CHOICES = Choices(
        ('APARTMENT', _('Apartment')),
        ('HOLIDAY_HOME', _('Holiday home')),
        ('SINGLE_FAMILY_HOME', _('Single family home')),
        ('COMMERCIAL', _('Commercial')),
    )
    type_of_property_listing = models.CharField(
        max_length = 50,
        choices = PROPERTY_LISTING_CHOICES,
        default = PROPERTY_LISTING_CHOICES.APARTMENT,)

    street = models.CharField(max_length=255)
    borough = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True, blank=True,)

    def __str__(self):
        return str(self.title)

class Contract(models.Model):
    rentalproperty = models.ForeignKey("RentalProperty", related_name='contracts', on_delete=models.CASCADE)
    insurance_required = models.BooleanField(default=True)
    other_terms = models.TextField(blank=True)

    def __str__(self):
        return str(self.insurance_required)
