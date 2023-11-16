import os

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import requests
from habit.models import Habit
from datetime import datetime

from habit.services import check_starting, get_mailing_time, check_frequency_weekly


@shared_task
def send_message():
    """
    Отправляет уведомления о привычках, которые нужно выполнить сегодня,
    предварительно сравнив текущее время и все привычки для выполнения.
    """

    # Определяем текущее время и день
    current_time = datetime.now().time()
    current_day = datetime.now().day

    # Получаем все имеющиеся привычки
    habits = Habit.objects.all()

    for habit in habits:
        check_starting(habit, current_day)

        # Разбиваем текущее время и время уведомления о привычке на дни, часы и минуты
        current_hour, current_minute = current_time.hour, current_time.minute
        habit_day, habit_hour, habit_minute = get_mailing_time(habit)

        # Сравниваем часы и минуты
        if (
            habit.is_starting
            and habit_day == current_day
            and current_hour == habit_hour
            and current_minute == habit_minute
        ):
            # Получаем сообщение о привычке
            message = habit.get_message()

            notifcation = habit.notification
            if notifcation == "email":
                # Отправляем уведомление на электронную почту пользователя
                subject = "Напоминание о необходимости выполнения привычки"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [habit.user.email]
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=False,
                )
            else:
                # Отправляем уведомление пользователю на Телеграм
                chat_id = habit.user.chat_id
                url = (
                    f"https://api.telegram.org/bot{os.getenv('TELEGRAM_API_TOKEN')}/sendMessage?"
                    f"chat_id={chat_id}&text={message}"
                )
                requests.get(url).json()

            check_frequency_weekly(habit)
