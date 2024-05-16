from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from gestion_etudiants.models import Student


class TestStudent(APITestCase):

    student = Student.objects.create(name='Student', age=20, grade='A')

    def test_list(self):
        student1 = Student.objects.create(name='Student1', age=20, grade='A')
        student2 = Student.objects.create(name='Student2', age=22, grade='B')

        url = reverse('student-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected = [
            {'id': student1.pk, 'name': student1.name, 'age': student1.age, 'grade': student1.grade},
            {'id': student2.pk, 'name': student2.name, 'age': student2.age, 'grade': student2.grade}
        ]
        self.assertEqual(expected, response.json())

    def test_create(self):
        url = reverse('student-list')
        response = self.client.post(url, data={'name': 'Nouvel étudiant', 'age': 21, 'grade': 'A'})

        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        new_student = Student.objects.get(name='Nouvel étudiant')
        self.assertIsNotNone(new_student)

    def test_update(self):
        update_url = reverse('student-detail', kwargs={'pk': self.student.pk})
        updated_data = {'name': 'UpdatedStudent', 'age': 26, 'grade': 'A'}
        response = self.client.put(update_url, data=updated_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'UpdatedStudent')
        self.assertEqual(self.student.age, 26)
        self.assertEqual(self.student.grade, 'A')

    def test_delete(self):
        delete_url = reverse('student-detail', kwargs={'pk': self.student.pk})
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Vérifie que l'étudiant a bien été supprimé de la base de données
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=self.student.pk)


