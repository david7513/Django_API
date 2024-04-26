from rest_framework import viewsets
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=404)
        student.delete()
        return Response(status=204)