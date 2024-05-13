import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from pytest_django.asserts import assertTemplateUsed
import pytest
from gestion_etudiants.models import Student
from gestion_etudiants.serializers import StudentSerializer

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_student():
    return Student.objects.create(name='David Coleman', age=23, grade='A')


def test_list_students(api_client, create_student):
    url = reverse('student-list')  # Arrange
    response = api_client.get(url)  # Act
    assert response.status_code == status.HTTP_200_OK  # Assert
    assert len(response.data) == 1  # Assert


def test_create_student(api_client):
    url = reverse('student-list')  # Arrange
    data = {'name': 'Jane Smith', 'age': 22, 'grade': 'B'}  # Arrange
    response = api_client.post(url, data, format='json')  # Act
    assert response.status_code == status.HTTP_201_CREATED  # Assert
    assert Student.objects.filter(name='Jane Smith').exists()  # Assert


def test_retrieve_student(api_client, create_student):
    student = create_student  # Arrange
    url = reverse('student-detail', kwargs={'pk': student.pk})  # Arrange
    response = api_client.get(url)  # Act
    assert response.status_code == status.HTTP_200_OK  # Assert
    assert response.data['name'] == 'David Coleman'  # Assert


def test_update_student(api_client, create_student):
    student = create_student  # Arrange
    url = reverse('student-detail', kwargs={'pk': student.pk})  # Arrange
    data = {'name': 'John Doe Jr.', 'age': 21, 'grade': 'A+'}  # Arrange
    response = api_client.put(url, data, format='json')  # Act
    assert response.status_code == status.HTTP_200_OK  # Assert
    updated_student = Student.objects.get(pk=student.pk)  # Act
    assert updated_student.name == 'John Doe Jr.'  # Assert
    assert updated_student.age == 21  # Assert
    assert updated_student.grade == 'A+'  # Assert


def test_delete_student(api_client, create_student):
    student = create_student  # Arrange
    url = reverse('student-detail', kwargs={'pk': student.pk})  # Act
    response = api_client.delete(url)  # Act
    assert response.status_code == status.HTTP_204_NO_CONTENT  # Assert
    assert not Student.objects.filter(pk=student.pk).exists()  # Assert
