from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

# Create your views here.
# kullanıcı giriş yapmışsa home sayfasını döndürüyorum
# logini zorunlu tutmak için login_required decorator kullanıyorum
# index.html'i bir layout olarak kullanıyorum ve bütün sayfalarımı bu layouta göre düzenliyorum
# bu layout sayesinde tüm sayfalarımın header ve footer kısmını tekrar tekrar yazmamış oluyorum
@api_view(['GET'])
@login_required
def home(request):
    return render(request, 'index.html')