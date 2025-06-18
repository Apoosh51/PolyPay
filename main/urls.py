from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about_bank/', views.about_bank, name='about_bank'),
    path('deposits/', views.deposits, name='deposits'),
]