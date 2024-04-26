from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ViewSet):
    def list(self, request):
        # Récupérer tous les étudiants depuis la base de données
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Créer un nouvel étudiant à partir des données fournies
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # Récupérer un étudiant spécifique par son ID
        queryset = Student.objects.all()
        student = queryset.get(pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def update(self, request, pk=None):
        # Mettre à jour les données d'un étudiant existant
        queryset = Student.objects.all()
        student = queryset.get(pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Supprimer un étudiant spécifique par son ID
        queryset = Student.objects.all()
        student = queryset.get(pk=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
