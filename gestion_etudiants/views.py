from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer

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

    def update(self, request, id=None):
        try:
            student = self.get_object(id=id)
        except Student.DoesNotExist:
            return Response({"message": "Étudiant introuvable"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, id=None):
        try:
            student = self.get_object(id=id)
        except Student.DoesNotExist:
            return Response({"message": "Étudiant introuvable"}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response({"message": "Étudiant supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
