from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from .models import Rent
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from iha.models import IHA
from django.contrib.auth.decorators import permission_required

@api_view(['GET', 'POST'])
@login_required
@permission_required('rent.add_rent')
def rent(request, iha_id):
    if request.method == 'POST':
            user_id = request.user.id
            iha_id = iha_id
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            rent_start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M'))
            rent_end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M'))

            # İlgili IHA ID'si için mevcut kiralama kayıtlarını kontrol et
            existing_rents = Rent.objects.filter(iha_id=iha_id)
            if existing_rents:
                for rent in existing_rents:
                    # Eğer seçilen tarih aralığı mevcut kiralamalarla çakışıyorsa uyarı ver
                    if (rent_start_date <= rent.rentEndDate) and (rent_end_date >= rent.rentStartDate):
                        messages.error(request, 'Seçilen tarih aralığı başka bir kiralama ile çakışıyor.')
                        return redirect('rent_iha', iha_id=iha_id)

            # Kiralama kaydını oluştur ve kaydet
            Rent.objects.create(iha_id=iha_id, user_id=user_id, rentStartDate=rent_start_date, rentEndDate=rent_end_date)
            messages.success(request, 'Kiralama işlemi başarılı.')
            return redirect('/iha/')
    else:
        return render(request, 'rent.html')
    
# my rent list method
@api_view(['GET'])
@login_required
@permission_required('rent.list_my_rents')
def my_rents(request):
    user_id = request.user.id
    rents = Rent.objects.filter(user_id=user_id)
    rent_list = []
    for rent in rents:
        rent_list.append({
            'id': rent.id,
            'iha_id': rent.iha_id,
            'iha_model': rent.iha.model,
            'rentStartDate': rent.rentStartDate,
            'rentEndDate': rent.rentEndDate
        })
    return render(request, 'my_rents.html', {'myrents': rent_list})

# admin rent list method
@api_view(['GET'])
@login_required
@permission_required('rent.list_admin_rents')
def admin_rents(request):
    rents = Rent.objects.all()
    rent_list = []
    for rent in rents:
        rent_list.append({
            'id': rent.id,
            'iha_id': rent.iha_id,
            'iha_model': rent.iha.model,
            'user_id': rent.user_id,
            'username': rent.user.username,
            'rentStartDate': rent.rentStartDate,
            'rentEndDate': rent.rentEndDate
        })
    return render(request, 'rent_list.html', {'rents': rent_list})

# admin rent delete method
@api_view(['GET'])
@login_required
@permission_required('rent.delete_admin_rent')
def admin_delete_rent(request, rent_id):
    try:
        Rent.objects.filter(id=rent_id).delete()
        messages.success(request, 'Kiralama kaydı silindi.')
        return redirect('admin_rent_list')
    except:
        messages.error(request, 'Kiralama kaydı silinemedi.')
        return redirect('admin_rent_list')
    
# rent delete method
@api_view(['GET'])
@login_required
@permission_required('rent.delete_my_rent')
def delete_rent(request, rent_id):
    try:
        Rent.objects.filter(id=rent_id).delete()
        messages.success(request, 'Kiralama kaydınız silindi.')
        return redirect('my_rents')
    except:
        messages.error(request, 'Kiralama kaydınız silinemedi.')
        return redirect('my_rents')
    
#admin_rent_update method
@api_view(['POST','GET',])
@login_required
@permission_required('rent.update_admin_rent')
def admin_update_rent(request,rent_id):
    rent = Rent.objects.get(id=rent_id)
    if request.method == 'POST':
        try:
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            rent_start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M'))
            rent_end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M'))
            rent.rentStartDate = rent_start_date
            rent.rentEndDate = rent_end_date

            # İlgili IHA ID'si için mevcut kiralama kayıtlarını kontrol et
            existing_rents = Rent.objects.filter(iha_id=request.POST.get('iha_id') and id != rent_id)
            if existing_rents:
                for rent in existing_rents:
                    # Eğer seçilen tarih aralığı mevcut kiralamalarla çakışıyorsa uyarı ver
                    if (rent_start_date <= rent.rentEndDate) and (rent_end_date >= rent.rentStartDate):
                        messages.error(request, 'Seçilen tarih aralığı başka bir kiralama ile çakışıyor.')
                        return redirect('admin_rent_update', rent_id=rent_id)
                    
            rent.iha_id = request.POST.get('iha_id')
            rent.user_id = request.POST.get('user_id')
            rent.save()
            messages.success(request, 'Kiralama kaydı güncellendi.')
            return redirect('admin_rent_list')
        except:
            messages.error(request, 'Kiralama kaydı güncellenemedi.')
            return redirect('admin_rent_update', rent_id=rent_id)
    else:
        rent = Rent.objects.get(id=rent_id)
        users = get_user_model().objects.all()
        ihas = IHA.objects.all()
        return render(request, 'rent_update.html',{'rent':rent,'ihas': ihas,'users':users})
    
#rent_update method
@api_view(['POST','GET'])
@login_required
@permission_required('rent.update_my_rent')
def update_rent(request,rent_id):
    rent = Rent.objects.get(id=rent_id)
    if request.method == 'POST':
        try:
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            rent_start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M'))
            rent_end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M'))
            rent.rentStartDate = rent_start_date
            rent.rentEndDate = rent_end_date

            # İlgili IHA ID'si için mevcut kiralama kayıtlarını kontrol et
            existing_rents = Rent.objects.filter(iha_id=request.POST.get('iha_id') and id != rent_id)
            if existing_rents:
                for rent in existing_rents:
                    # Eğer seçilen tarih aralığı mevcut kiralamalarla çakışıyorsa uyarı ver
                    if (rent_start_date <= rent.rentEndDate) and (rent_end_date >= rent.rentStartDate):
                        messages.error(request, 'Seçilen tarih aralığı başka bir kiralama ile çakışıyor.')
                        return redirect('my_rent_update', rent_id=rent_id)
                    
            rent.iha_id = request.POST.get('iha_id')
            rent.save()
            messages.success(request, 'Kiralama kaydı güncellendi.')
            return redirect('my_rents')
        except:
            messages.error(request, 'Kiralama kaydı güncellenemedi.')
            return redirect('my_rent_update', rent_id=rent_id)
    else:
        rent = Rent.objects.get(id=rent_id)

        # Eğer gelen rent nesnesinin user_id'si ile login olan kullanıcının id'si farklı ise
        if rent.user_id != request.user.id:
            return redirect('my_rent')  # Yönlendirme yapılacak hata sayfasının adını buraya yazın

        ihas = IHA.objects.all()
        return render(request, 'my_rent_update.html',{'rent':rent,'ihas': ihas})