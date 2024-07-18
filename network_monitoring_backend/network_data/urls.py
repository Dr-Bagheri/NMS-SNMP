from django.urls import path
from . import views

urlpatterns = [
    path('api/data/', views.receive_snmp_data, name='receive_snmp_data'),
]