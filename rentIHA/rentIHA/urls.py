from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, re_path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/register/', views.register, name='register'),
    path('', include('layout.urls')),
    path('iha/', include('iha.urls')),
    path('rent/', include('rent.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    # bu path ile eğer hiçbir path eşleşmezse home sayfasına yönlendiriyorum
    re_path(r'^.*$', lambda request: redirect('home')), #wildcard
]
