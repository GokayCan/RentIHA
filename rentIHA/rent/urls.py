from django.urls import path
from . import views

# my ile devam eden sayfalar kullanıcının kendi kiraladığı IHA'ları görebileceği ve işlem yapabileceği sayfalardır
# admin ile devam eden sayfalar ise adminin tüm kiralama işlemlerini görebileceği ve işlem yapabileceği sayfalardır
# admin iki sayfayada erişebilirken user sadece my ile başlayan sayfalara erişebilir
# rent_iha ise IHA kiralama işlemlerinin yapıldığı sayfadır bu yüzden iki tarafta erişebilir
urlpatterns = [
    path('<int:iha_id>/', views.rent, name='rent_iha'),
    path('rents/', views.admin_rents, name='admin_rent_list'),
    path('rents/delete/<int:rent_id>/', views.admin_delete_rent, name='admin_rent_delete'),
    path('rents/update/<int:rent_id>/', views.admin_update_rent, name='admin_rent_update'),
    path('my_rents/', views.my_rents, name='my_rents'),
    path('my_rents/delete/<int:rent_id>/', views.delete_rent, name='my_rents_delete'),
    path('my_rents/update/<int:rent_id>/', views.update_rent, name='my_rents_update'),
]   