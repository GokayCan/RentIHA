from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_ihas, name='iha_list'),
    path('add/', views.add_iha, name='iha_add'),
    path('update/<int:iha_id>/', views.update_iha, name='iha_update'),
    path('get/', views.list_ihas_data, name='iha_list_data'),
    path('delete/', views.delete_iha, name='iha_delete'),
]   