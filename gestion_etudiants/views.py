from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from django.shortcuts import get_object_or_404

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()   # Récupère tous les objets Student de la base de données
    serializer_class = StudentSerializer  # Utilise le serializer StudentSerializer pour la sérialisation

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None, *args, **kwargs):
        queryset = self.get_queryset()
        student = queryset.get(id=id)
        serializer = self.get_serializer(student)
        return Response(serializer.data)

    def put(request, id):
        student = get_object_or_404(Student, id=id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(request, id):
        student = get_object_or_404(Student, id=id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def search_by_name(self, request, name=None):
        if name:
            students = Student.objects.filter(name__icontains=name)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        else:
            return Response("Please provide a name parameter in the URL", status=status.HTTP_400_BAD_REQUEST)