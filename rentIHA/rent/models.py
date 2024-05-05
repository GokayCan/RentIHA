from django.db import models
from django.contrib.auth.models import User
from iha.models import IHA

# Create your models here.
class Rent(models.Model):
    # kiralamaya ait ilişkili olan tabloların tanımlamaları yapılıyor
    # iha,iha tablosuyla olan ilişkiyi belirtiyor, bu sayede iha_id elde ediyorum
    iha = models.ForeignKey(IHA, on_delete=models.PROTECT, related_name='rent_iha')
    # user,user tablosuyla olan ilişkiyi belirtiyor, bu sayede user_id elde ediyorum
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rent_user')
    # burada hem tarih hem saat bilgisi tutuluyor
    rentStartDate = models.DateTimeField()
    rentEndDate = models.DateTimeField()

    # bu kısım modelin permissionlarını belirlemek için kullanılıyor,
    class Meta:
        permissions = ( ("list_my_rents",""), ("list_admin_rents",""), ("delete_my_rent",""), ("delete_admin_rent",""), ("update_my_rent",""), ("update_admin_rent",""))