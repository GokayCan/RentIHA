from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import redirect, render
from iha.models import IHA
from django.contrib import messages
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rent.models import Rent
from django.contrib.auth.decorators import permission_required

# bu method ile iha listesini döndürüyorum ve login olmayan kullanıcıların erişimini engelliyorum
# aynı zamanda iha.list_ihas izni olan kullanıcıların erişimini sağlıyorum örneğin admin ve user grubu bu methoda erişebilir
@api_view(['GET'])
@login_required
@permission_required('iha.list_ihas')
def list_ihas(request):
    ihas = IHA.objects.all()
    # messages.info(request, 'Listeleme İşlemi Başarılı')
    return render(request, 'iha_list.html', {'ihas': ihas,'message': 'Listeleme İşlemi Başarılı'})

# bu method ile iha listesini json formatında döndürüyorum ve login olmayan kullanıcıların erişimini engelliyorum
# bunu yapma sebebim eğer listeden bir iha silinirse sayfa refresh edilmeden silme işlemi gerçekleştirdikten sonra listede güncelleme yapabilmek için
@api_view(['GET'])
@login_required
@permission_required('iha.list_ihas_data')
def list_ihas_data(request):
    ihas = IHA.objects.all()
    # messages.info(request, 'Listeleme İşlemi Başarılı')
    return JsonResponse({'ihas': list(ihas.values())})

# bu method ile iha ekliyorum
@api_view(['POST','GET'])
@login_required
@permission_required('iha.add_iha')
def add_iha(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        weight = request.POST.get('weight')
        category = request.POST.get('category')
        new_iha = IHA(brand=brand, model=model, weight=weight, category=category)
        new_iha.save()
        messages.success(request, 'Ekleme İşlemi Başarılı')
        return redirect('/iha/')
    else:
        return render(request, 'iha_add.html')

# bu method ile iha güncelliyorum hangi ihanın güncelleneceğini iha_id ile belirtiyorum
@api_view(['POST','GET'])
@login_required
@permission_required('iha.update_iha')
def update_iha(request, iha_id):
    iha = IHA.objects.get(id=iha_id)
    if request.method == 'POST':
        iha.brand = request.POST.get('brand')
        iha.model = request.POST.get('model')
        iha.weight = request.POST.get('weight')
        iha.category = request.POST.get('category')
        iha.save()
        messages.info(request, 'Güncelleme İşlemi Başarılı')
        return redirect('/iha/')
    else:
        return render(request, 'iha_update.html', {'iha': iha})

# bu method ile iha siliyorum ve hangi ihanın silineceğini iha_id ile belirtiyorum
@api_view(['POST'])
@login_required
@permission_required('iha.delete_iha')
def delete_iha(request):
    iha_id = request.POST.get('iha_id')
    iha = IHA.objects.get(id=iha_id)
    rents = Rent.objects.filter(iha_id=iha.id)
    # eğer bir kiralama durumu daha bitmemiş ise iha silinemez
    if rents.exists() and any(rent.rentEndDate >= timezone.now() for rent in rents):
        messages.warning(request, 'Silme İşlemi Başarısız. İHA, kiralanmış durumdadır.')
        return JsonResponse({'status':'false','message': 'Silme İşlemi Başarısız. İHA, kiralanmış durumdadır.'})
    else:    
        iha.delete()
        # messages.success(request, 'Silme İşlemi Başarılı')
        # messages.info(request, 'Silme İşlemi Başarılı')
        return JsonResponse({'status':'true','message': 'Silme İşlemi Başarılı'})