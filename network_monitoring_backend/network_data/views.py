from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DeviceData
from .serializers import DeviceDataSerializer

@api_view(['POST'])
def receive_snmp_data(request):
    if request.method == 'POST':
        serializer = DeviceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data received successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)