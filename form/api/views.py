# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobApplicationSerializer  # Serializer'ı içe aktarın


class JobApplicationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Başvuruyu kaydedin
            return Response(
                {"message": "Başvuru başarılı!"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)