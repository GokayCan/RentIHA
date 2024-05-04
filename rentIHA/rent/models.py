from django.db import models
from django.contrib.auth.models import User
from iha.models import IHA

# Create your models here.
class Rent(models.Model):
    iha = models.ForeignKey(IHA, on_delete=models.PROTECT, related_name='rent_iha')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rent_user')
    rentStartDate = models.DateTimeField()
    rentEndDate = models.DateTimeField()

    class Meta:
        permissions = ( ("list_my_rents",""), ("list_admin_rents",""), ("delete_my_rent",""), ("delete_admin_rent",""), ("update_my_rent",""), ("update_admin_rent",""))