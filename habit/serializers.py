from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import timedelta

from habit.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    """
    Сериализатор для модели Habit.
    """

    def validate(self, data):
        # Проверка одновременного выбора связанной привычки и указания вознаграждения
        if data.get("related_habit") and data.get("reward"):
            raise ValidationError(
                "Нельзя одновременно выбирать связанную привычку и указывать вознаграждение"
            )

        # Проверка времени выполнения
        if data.get("estimated_time"):
            estimated_time_seconds = int(data["estimated_time"])
            if estimated_time_seconds > 120:
                raise ValidationError("Время выполнения не должно превышать 120 секунд")

        # Проверка связанных привычек
        if data.get("related_habit") and not data["related_habit"].is_pleasant:
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки"
            )

        # Проверка приятной привычки
        if data.get("is_reward"):
            if data.get("related_habit") or data.get("reward"):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки"
                )

        # Проверка периодичности привычки
        if data.get("frequency"):
            frequency_str = data[
                "frequency"
            ].lower()  # Преобразуем значение в нижний регистр для удобства проверки
            frequencies = {
                "daily": timedelta(days=1),
                "weekly": timedelta(days=7),
            }
            if frequency_str in frequencies:
                frequency = frequencies[frequency_str]
                if frequency < timedelta(days=7):
                    raise ValidationError(
                        "Нельзя выполнять привычку реже, чем 1 раз в 7 дней"
                    )
            else:
                raise ValidationError("Неподдерживаемое значение периодичности")

        return data

    class Meta:
        model = Habit
        fields = "__all__"
