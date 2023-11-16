from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings
import os

User = get_user_model()


class Command(BaseCommand):
    """
    Команда Django для создания или обновления суперпользователя
    """

    def handle(self, *args, **kwargs):
        """
        Обработчик команды
        :param args: дополнительные аргументы
        :param kwargs: дополнительные именованные аргументы
        """
        User.objects.filter(
            is_superuser=True
        ).delete()  # удаление существующего суперпользователя, если таковой есть

        super_user, created = User.objects.get_or_create(
            email=settings.EMAIL_HOST_USER,
            defaults={
                "first_name": "Admin",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
                "chat_id": os.getenv("CHAT_ID_ADMIN"),
                "is_active": True,
            },
        )  # получение или создание суперпользователя

        if created:
            super_user.set_password(
                os.getenv("ADMIN_PASSWORD")
            )  # установка пароля для суперпользователя
            super_user.save()  # сохранение изменений
