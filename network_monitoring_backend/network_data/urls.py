from django.urls import path
from . import views  
from .views import delete_post

urlpatterns = [
    path('api/data/', views.device_data, name='device_data'),  
    path('post/delete/<int:post_id>/', delete_post, name='delete_post'),
]