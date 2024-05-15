from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from gestion_etudiants.models import Student


class TestStudent(APITestCase):
    url = reverse_lazy('student-list')
    student = Student.objects.create(name='Student', age=20, grade='A')

    def test_list(self):
        # Créer deux étudiants pour tester la liste
        student1 = Student.objects.create(name='Student1', age=20, grade='A')
        student2 = Student.objects.create(name='Student2', age=22, grade='B')

        # Effectuer une requête GET pour récupérer la liste des étudiants
        response = self.client.get(self.url)

        # Vérifier que le statut de la réponse est 200 (succès)
        self.assertEqual(response.status_code, 200)

        # Préparer les données attendues pour le test
        expected = [
            {
                'id': student1.pk,
                'name': student1.name,
                'age': student1.age,
                'grade': student1.grade,
            },
            {
                'id': student2.pk,
                'name': student2.name,
                'age': student2.age,
                'grade': student2.grade,
            }
        ]

        # Vérifier que les données retournées correspondent aux attentes
        self.assertEqual(expected, response.json())

    def test_create(self):
        # Vérifier qu'aucun étudiant n'existe avant de tenter d'en créer un
        self.assertFalse(Student.objects.exists())

        # Effectuer une requête POST pour tenter de créer un étudiant
        response = self.client.post(self.url, data={'name': 'Nouvel étudiant', 'age': 21, 'grade': 'A'})

        # Vérifier que le statut de la réponse est bien 415 (méthode non autorisée pour la création)
        self.assertEqual(response.status_code, 415)

        # Vérifier qu'aucun nouvel étudiant n'a été créé malgré le statut 415
        self.assertFalse(Student.objects.exists())

    def test_update(self):
        # Effectuer une requête PUT pour mettre à jour les informations de l'étudiant
        update_url = reverse_lazy('student-detail', kwargs={'pk': self.student.pk})
        updated_data = {'name': 'UpdatedStudent', 'age': 26, 'grade': 'A'}
        response = self.client.put(update_url, data=updated_data)

        # Vérifier que le statut de la réponse est 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que les informations de l'étudiant ont été correctement mises à jour dans la base de données
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'UpdatedStudent')
        self.assertEqual(self.student.age, 26)
        self.assertEqual(self.student.grade, 'A')

    def test_delete(self):
        # Effectuer une requête DELETE pour supprimer l'étudiant
        delete_url = reverse_lazy('student-detail', kwargs={'pk': self.student.pk})
        response = self.client.delete(delete_url)

        # Vérifier que le statut de la réponse est 204 (No Content) après la suppression
        self.assertEqual(response.status_code, status.HTTP_404_NO_CONTENT)

        # Vérifier que l'étudiant a bien été supprimé de la base de données
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=self.student.pk)