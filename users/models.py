from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя
    """

    username = None  # отключение использования имени пользователя
    email = models.EmailField(
        unique=True, verbose_name="электронная почта"
    )  # поле для email
    avatar = models.ImageField(
        upload_to="users/", verbose_name="аватар", null=True, blank=True
    )  # поле для аватара пользователя
    phone = models.CharField(
        max_length=35, verbose_name="номер телефона"
    )  # поле для номера телефона
    city = models.CharField(
        max_length=50, verbose_name="город", null=True, blank=True
    )  # поле для города
    chat_id = models.CharField(
        max_length=20, default=0, verbose_name="чат-ID в Telegram"
    )  # поле для идентификатора чата в Telegram

    USERNAME_FIELD = "email"  # поле, используемое для входа в систему
    REQUIRED_FIELDS = []  # обязательные поля при создании пользователя

    objects = UserManager()
