from django.urls import path
from . import views

urlpatterns = [
    path('',views.test,name='test'),
    path('home/',views.home,name='home'),
    path('qr/',views.qr,name='qr'),
    path('report/',views.reports, name="reports"),
    
]
