from django.urls import path
from . import views

# path boşta olsa home da olsa aynı yere yönlendiriyorum
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
]