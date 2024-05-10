from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DeviceData
from .models import Post
from .serializers import DeviceDataSerializer
from django.http import HttpResponse
from django.db.models import Subquery, OuterRef


def get_latest_device_data():
    latest_entries = DeviceData.objects.filter(
        device_id=OuterRef('device_id')
    ).order_by('-timestamp')

    return DeviceData.objects.annotate(
        latest_id=Subquery(latest_entries.values('id')[:1])
    ).filter(
        id=OuterRef('latest_id')
    ).distinct()
    
    
@api_view(['GET', 'POST'])
def device_data(request):
    # Handling GET requests to fetch device data
    if request.method == 'GET':
        data = DeviceData.objects.all()
        serializer = DeviceDataSerializer(data, many=True)
        return Response(serializer.data)

    # Handling POST request to create new device data
    elif request.method == 'POST':
        serializer = DeviceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

def delete_post(request, post_id):
    
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
   

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('name_of_your_home_page_view')  # Redirect to a desired URL