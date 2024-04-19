from enum import Enum

from django.db import models
from django.contrib.auth.models import User

# from common.models import BaseUUIDModel


class ProductCategory(models.Model):

    class TypeBilling(Enum):
        BILLING_TONNE = 'Facturation à la tonne'
        BILLING_WEIGHED = 'Facturation à la pesée'

    wording = models.CharField(max_length=100)
    billing_type = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in TypeBilling])