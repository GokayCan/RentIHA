from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model,login,authenticate
from django.contrib import messages
from django.contrib.auth.models import Group

@api_view(['POST','GET'])
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş yapıldı.')
            return redirect('/home')
        else:
            messages.warning(request, 'Kullanıcı adı veya şifre hatalı.')
            return redirect('auth/login')
    else:
        return render(request, 'login.html')
    
@api_view(['GET'])
def logout_user(request):
    request.session.flush()
    messages.info(request, 'Çıkış yapıldı.')
    return redirect('/auth/login')

@api_view(['POST','GET'])
def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Zaten giriş yapmışsınız.')
        return redirect('/home')
    
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
            group = Group.objects.get(name='user_group')
            user.groups.add(group)
            messages.success(request, 'Kayıt başarılı.')
            return redirect('/auth/login')
        except Exception as e:
            messages.warning(request, 'Kayıt başarısız.')
            return redirect('/auth/register')
    else:
        return render(request, 'register.html')