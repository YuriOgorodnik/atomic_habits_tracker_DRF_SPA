from django.db import models

from users.models import User


class Habit(models.Model):
    """
    Модель, представляющая привычку пользователя.
    """

    NOTIFICATION_TIME_CHOICES = [
        ("fifteen", "за 15 минут"),
        ("thirty", "за 30 минут"),
        ("hour", "за час"),
        ("two_hours", "за 2 часа"),
        ("day", "за 24 часа"),
    ]

    FREQUENCY_CHOICES = [
        ("daily", "ежедневная"),
        ("weekly", "еженедельная"),
    ]

    WEEKDAY_CHOICES = [
        ("today", "сегодня"),
        ("tomorrow", "завтра"),
    ]

    NOTIFICATION_CHOICES = [
        ("telegram", "телеграм"),
        ("email", "электронная почта"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    place = models.CharField(max_length=255, verbose_name="место выполнения")
    notification_time = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TIME_CHOICES,
        default="thirty",
        verbose_name="уведомление до начала привычки",
    )
    time = models.TimeField(verbose_name="время выполнения привычки")
    action = models.CharField(max_length=255, verbose_name="действие (привычка)")
    is_reward = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="cвязанная привычка",
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default="daily",
        verbose_name="периодичность выполнения привычки",
    )
    weekday = models.CharField(
        max_length=20,
        choices=WEEKDAY_CHOICES,
        default="today",
        verbose_name="cтарт выполнения привычки",
    )
    reward = models.CharField(
        max_length=255, blank=True, verbose_name="вознаграждение за выполнение привычки"
    )
    estimated_time = models.IntegerField(verbose_name="время на выполнение привычки")
    is_public = models.BooleanField(
        default=False, verbose_name="признак публичности привычки"
    )
    date_of_start = models.DateField(
        auto_now_add=True, verbose_name="дата начала привычки"
    )
    is_starting = models.BooleanField(
        default=False, verbose_name="признак начала рассылки"
    )
    notification = models.CharField(
        max_length=20,
        choices=NOTIFICATION_CHOICES,
        default="telegram",
        verbose_name="метод оповещения",
    )

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def get_message(self):
        """
        Возвращает сообщение, описывающее привычку.

        Если привычка является приятной, то сообщение включает информацию о действии, времени, месте и
        вознаграждении.
        В противном случае, сообщение содержит информацию только о
        привычке, времени и месте её выполнения.
        """
        if self.is_reward:
            message = (
                f"Я буду {self.action} в {self.time} в {self.place}.\n"
                f"На это мне отведено {self.estimated_time} минут.\n"
                f"Вознаграждение: {self.reward}."
            )
        else:
            message = (
                f"Я буду {self.action} в {self.time} в {self.place}.\n"
                f"На это мне отведено {self.estimated_time} минут.\n"
            )

        return message
