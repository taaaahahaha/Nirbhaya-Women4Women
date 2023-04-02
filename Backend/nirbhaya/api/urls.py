from django.urls import path
from . import views

urlpatterns = [
    path('',views.test,name='test'),
    path('home/',views.home,name='home'),
    path('qr/',views.qr,name='qr'),
    path('reports/',views.reports, name="reports"),
    path('sos/',views.sos, name="sos"),
    path('safespaces/',views.safespaces, name="safespaces"),
    path('profile/',views.profile, name="profile"),
    
]
