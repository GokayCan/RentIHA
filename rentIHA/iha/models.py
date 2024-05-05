from django.db import models

# Create your models here.
class IHA(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)
    category = models.CharField(max_length=100)

    # bu kısım modelin permissionlarını belirlemek için kullanılıyor,
    # halihazırda zaten otomatik yükleniyor ama ben isimleri kendim belirlemek istedim
    class Meta:
        permissions = (("list_ihas",""), ("list_ihas_data",""),("update_iha",""))