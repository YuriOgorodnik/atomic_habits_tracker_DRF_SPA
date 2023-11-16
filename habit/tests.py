from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from habit.models import Habit
from users.models import User


class HabitTestsView(APITestCase):
    def setUp(self):
        """
        Подготовка тестовых данных: создание пользователя и привычки для тестирования.
        """
        self.user = User.objects.create_user(
            email="test@example.com", phone="12815365", chat_id="125648"
        )
        self.client.force_authenticate(user=self.user)
        self.related_habit = None
        self.habit = Habit.objects.create(
            user=self.user,
            place="test place",
            notification_time="thirty",
            time="07:00:00",
            action="Тестовая привычка",
            is_reward=False,
            related_habit=self.related_habit,
            frequency="daily",
            weekday="today",
            reward="Награда за связанную привычку",
            estimated_time=40,
            is_public=True,
            date_of_start="2023-11-15",
            is_starting=True,
            notification="telegram",
        )

    def test_habit_list_view(self):
        """
        Тестирование представления списка привычек.
        """
        url = reverse("habit:habit_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create_view(self):
        """
        Тестирование представления создания привычки.
        """
        self.user = User.objects.create_user(
            email="test1@example.com", phone="12815366", chat_id="125647"
        )
        self.client.force_authenticate(user=self.user)

        url = reverse("habit:habit_create")

        # Подготовка данных для создания привычки
        data = {
            "user": self.user.id,
            "place": "test1 place",
            "notification_time": "thirty",
            "time": "08:00:00",
            "action": "Тестовая привычка1",
            "is_pleasant": True,
            "is_reward": False,
            "frequency": "weekly",
            "reward": "",
            "estimated_time": 100,
            "is_public": True,
            "date_of_start": "2023-11-15",
            "is_starting": True,
            "notification": "telegram",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_habit_retrieve_view(self):
        """
        Тестирование представления получения информации о привычке.
        """
        self.user = User.objects.create_user(
            email="test3@example.com", phone="12815368", chat_id="125645"
        )
        self.client.force_authenticate(user=self.user)

        url = reverse("habit:habit_detail", kwargs={"pk": self.habit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update_view(self):
        """
        Тестирование представления обновления информации о привычке.
        """
        self.user = User.objects.create_user(
            email="test4@example.com", phone="12815369", chat_id="125644"
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            place="test3 place",
            notification_time="thirty",
            time="07:00:00",
            action="Тестовая привычка3",
            is_reward=False,
            related_habit=self.related_habit,
            frequency="daily",
            weekday="today",
            reward="Награда за связанную привычку3",
            estimated_time=40,
            is_public=True,
            date_of_start="2023-11-15",
            is_starting=True,
            notification="telegram",
        )

        # Подготовка данных для обновления созданной привычки
        update_data = {
            "user": self.user.id,
            "place": "test3 place",
            "notification_time": "thirty",
            "time": "08:00:00",
            "action": "Обновленная тестовая привычка3",
            "is_pleasant": True,
            "is_reward": False,
            "frequency": "weekly",
            "reward": "",
            "estimated_time": 100,
            "is_public": True,
            "date_of_start": "2023-11-15",
            "is_starting": True,
            "notification": "telegram",
        }

        url = reverse("habit:habit_update", kwargs={"pk": self.habit.id})
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Habit.objects.get(id=self.habit.id).action, "Обновленная тестовая привычка3"
        )

    def test_habit_destroy_view(self):
        """
        Тестирование представления удаления привычки.
        """
        url = reverse("habit:habit_delete", kwargs={"pk": self.habit.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_public_habit_list_view(self):
        """
        Тестирование представления списка публичных привычек.
        """
        url = reverse("habit:habit_public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_validate_related_habit_and_reward(self):
        """
        Тестирование одновременного выбора связанной привычки и указании вознаграждения.
        """
        self.user = User.objects.create_user(
            email="test4@example.com", phone="25815367", chat_id="1412646"
        )
        self.client.force_authenticate(user=self.user)

        url = reverse("habit:habit_create")

        # Подготовка данных для создания привычки с неверными данными
        data = {
            "user": self.user.id,
            "place": "test4 place",
            "notification_time": "thirty",
            "time": "09:00:00",
            "action": "Тестовая привычка4",
            "is_reward": False,
            "related_habit": self.related_habit,
            "frequency": "daily",
            "weekday": "today",
            "reward": "Награда за связанную привычку4",
            "estimated_time": 40,
            "is_public": True,
            "date_of_start": "2023-11-15",
            "is_starting": True,
            "notification": "telegram",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_validate_estimated_time_exceeds_120_seconds(self):
        """
        Тестирование превышения времени выполнения привычки.
        """
        self.user = User.objects.create_user(
            email="test5@example.com", phone="223125367", chat_id="12564612"
        )
        self.client.force_authenticate(user=self.user)

        url = reverse("habit:habit_create")

        # Подготовка данных для создания привычки с неверными данными
        data = {
            "user": self.user.id,
            "place": "test5 place",
            "notification_time": "thirty",
            "time": "09:00:00",
            "action": "Тестовая привычка5",
            "is_reward": False,
            "related_habit": self.related_habit,
            "frequency": "daily",
            "weekday": "today",
            "estimated_time": 50,
            "is_public": True,
            "date_of_start": "2023-11-15",
            "is_starting": True,
            "notification": "telegram",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_validate_related_habit_is_pleasant(self):
        """
        Тестирование попадания в связанные привычки
        привычек с отсутствующим признаком приятной привычки.
        """
        self.user = User.objects.create_user(
            email="test6@example.com", phone="223125322", chat_id="12564633"
        )
        self.client.force_authenticate(user=self.user)

        url = reverse("habit:habit_create")

        # Подготовка данных для создания привычки с неверными данными
        data = {
            "user": self.user.id,
            "place": "test6 place",
            "notification_time": "thirty",
            "time": "09:00:00",
            "action": "Тестовая привычка6",
            "is_reward": False,
            "related_habit": self.related_habit,
            "frequency": "daily",
            "weekday": "today",
            "estimated_time": 70,
            "is_public": True,
            "date_of_start": "2023-11-15",
            "is_starting": True,
            "notification": "telegram",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_validate_pleasant_habit_has_no_related_habit_or_reward(self):
        """
        Тестирование наличия у приятной привычки связанной привычки или вознаграждения.
        """
        self.user = User.objects.create_user(
            email="test6@example.com", phone="223125322", chat_id="12564633"
        )
        self.client.force_authenticate(user=self.user)

        url = reverse("habit:habit_create")

        # Подготовка данных для создания привычки с неверными данными
        data = {
            "user": self.user.id,
            "place": "test6 place",
            "notification_time": "thirty",
            "time": "09:00:00",
            "action": "Тестовая привычка6",
            "is_reward": True,
            "related_habit": self.related_habit,
            "frequency": "daily",
            "weekday": "today",
            "reward": "Награда за привычку6",
            "estimated_time": 60,
            "is_public": True,
            "date_of_start": "2023-11-15",
            "is_starting": True,
            "notification": "telegram",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
