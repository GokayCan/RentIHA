from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model,login,authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import Group

# Kullanıcı giriş methodu kullanıcadan kullanıcı ve şifre bilgisi alıp djangonun hazır auth methodları yardımıyla kullanıcının login işlemini yapıyorum
@api_view(['POST','GET'])
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # veriler formdan alındıktan sonra authenticate methodu ile kullanıcı bilgileri kontrol ediliyor ve kullanıcıya ait bir obje dönüyor
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # eğer kullanıcı varsa yani dbde böyle bir kullanıcı mevcutsa login methodu ile kullanıcı oturumu açılıyor ve sonucunda bir session yaratılıyor.
            login(request, user)
            messages.success(request, 'Giriş yapıldı.')
            return redirect('/home')
        else:
            # eğer kullanıcı yoksa hata mesajı döndürülüyor
            messages.warning(request, 'Kullanıcı adı veya şifre hatalı.')
            return redirect('auth/login')
    else:
        # method get olarak tetiklenirse login sayfası döndürülüyor
        return render(request, 'login.html')

# kullanıcın oturumunu sonlandıran method
@api_view(['GET'])
def logout_user(request):
    # istersek elimizle sessionı silebiliriz istersek djangonun hazır logout methodu ile sessionı silebiliriz
    #request.session.flush()
    logout(request)
    messages.info(request, 'Çıkış yapıldı.')
    return redirect('/auth/login')

# kullanıcı kayıt methodu
@api_view(['POST','GET'])
def register(request):
    # eğer kullanıcı zaten giriş yapmışsa home sayfasına yönlendiriyorum
    if request.user.is_authenticated:
        messages.warning(request, 'Zaten giriş yapmışsınız.')
        return redirect('/home')
    # eğer post methodu ile tetiklenirse kullanıcı bilgilerini alıp db ye kaydediyorum
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # E-posta ve kullanıcı adı kontrolü
        if get_user_model().objects.filter(username=username).exists():
            messages.warning(request, 'Bu kullanıcı adı zaten kullanılıyor.')
            return redirect('/auth/register')

        if get_user_model().objects.filter(email=email).exists():
            messages.warning(request, 'Bu e-posta adresi zaten kullanılıyor.')
            return redirect('/auth/register')


        try:
            user = get_user_model().objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            user.save()
            # kullanıcı kaydedildikten sonra kullanıcıya bir grup atıyorum bu grup ile kullanıcıların yetkilerini kontrol edebilirim
            group = Group.objects.get(name='user_group')
            user.groups.add(group)
            messages.success(request, 'Kayıt başarılı.')
            return redirect('/auth/login')
        except Exception as e:
            messages.warning(request, 'Kayıt başarısız.')
            return redirect('/auth/register')
    else:
        return render(request, 'register.html')