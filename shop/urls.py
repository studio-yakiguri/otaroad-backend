from django.urls import path

from . import views

urlpatterns = [
    path('shopinfo', views.ShopInfo.as_view()),
]