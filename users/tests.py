from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User


class UserAPITest(APITestCase):
    """
    Тестирование представлений для пользователей.
    """

    def setUp(self):
        """
        Устанавливаем объекты, необходимые для тестирования.
        """
        self.user = User.objects.create_user(
            email="test@example.com", phone="12815365", chat_id="125648"
        )

    def test_user_list_view(self):
        """
        Тестирование представления списка пользователей.
        """
        url = reverse("users:user_list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create_view(self):
        """
        Тестирование представления создания пользователя.
        """
        url = reverse("users:user_create")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "password2": "newpassword",
            "phone": "1234567890",
            "chat_id": "120203",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.get(email="newuser@example.com").phone, "1234567890"
        )

    def test_user_retrieve_view(self):
        """
        Тестирование представления получения информации о пользователе.
        """
        url = reverse("users:user_detail", kwargs={"pk": self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_view(self):
        """
        Тестирование представления обновления информации о пользователе.
        """
        url = reverse("users:user_update", kwargs={"pk": self.user.id})
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "updated@example.com",
            "phone": "9876543210",
            "chat_id": "1123514",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.user.id).phone, "9876543210")

    def test_user_destroy_view(self):
        """
        Тестирование представления удаления пользователя.
        """
        url = reverse("users:user_delete", kwargs={"pk": self.user.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
