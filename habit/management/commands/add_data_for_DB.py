import os

from django.core.management import BaseCommand

from habit.models import Habit
from users.models import User


class Command(BaseCommand):
    """
    Команда для удаления старых данных и добавления новых данных в базу данных Habit.

    Метод `handle` выполняет следующие шаги:
    - удаляет все записи в моделях User, Habit;
    - создаёт двух пользователей и три полезные привычки для каждого пользователя.
    """

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Habit.objects.all().delete()

        try:
            # Создаем пользователей и их привычки
            user_data = [
                {
                    "email": "yuri.ogorodnik@mail.ru",
                    "phone": "123456789",
                    "city": "Bobruisk",
                    "first_name": "Yuri",
                    "last_name": "Ogorodnik",
                    "chat_id": os.getenv("CHAT_ID_USER"),
                    "habits": [
                        {
                            "place": "гостинной",
                            "time": "06:00:00",
                            "action": "делать утреннюю зарядку",
                            "is_reward": False,
                            "frequency": "daily",
                            "reward": "можно выпить стакан воды после зарядки",
                            "estimated_time": 15,
                            "is_public": False,
                            "notification": "telegram",
                        },
                        {
                            "place": "кухне",
                            "time": "06:30:00",
                            "action": "готовить полезный завтрак",
                            "is_reward": True,
                            "frequency": "daily",
                            "reward": "можно выпить свежевыжатый сок",
                            "estimated_time": 30,
                            "is_public": False,
                            "notification": "telegram",
                        },
                        {
                            "place": "парке",
                            "time": "18:30:00",
                            "action": "кататься на велосипеде",
                            "is_reward": True,
                            "frequency": "weekly",
                            "reward": "можно съесть пироженое после прогулки",
                            "estimated_time": 60,
                            "is_public": True,
                            "notification": "telegram",
                        },
                    ],
                },
                {
                    "email": "galmak.sasha@mail.ru",
                    "phone": "987654321",
                    "city": "Minsk",
                    "first_name": "Alexandr",
                    "last_name": "Galmak",
                    "chat_id": os.getenv("CHAT_ID_USER"),
                    "habits": [
                        {
                            "place": "спортзале",
                            "time": "07:00:00",
                            "action": "заниматься йогой",
                            "is_reward": True,
                            "frequency": "weekly",
                            "reward": "после йоги можно побаловать себя соком",
                            "estimated_time": 30,
                            "is_public": True,
                            "notification": "email",
                        },
                        {
                            "place": "доме",
                            "time": "21:00:00",
                            "action": "медитировать",
                            "is_reward": True,
                            "frequency": "daily",
                            "reward": "выпить чашку чая после медитации",
                            "estimated_time": 20,
                            "is_public": False,
                            "notification": "email",
                        },
                        {
                            "place": "спортзале",
                            "time": "18:30:00",
                            "action": "тренироваться с тренером",
                            "is_reward": False,
                            "frequency": "weekly",
                            "reward": "после тренировки позвольте себе кислородный коктейль",
                            "estimated_time": 45,
                            "is_public": True,
                            "notification": "email",
                        },
                    ],
                },
            ]

            for user_info in user_data:
                user = User.objects.create(
                    email=user_info["email"],
                    phone=user_info["phone"],
                    city=user_info["city"],
                    first_name=user_info["first_name"],
                    last_name=user_info["last_name"],
                    chat_id=user_info["chat_id"],
                )
                user.set_password(os.getenv("ADMIN_PASSWORD"))
                user.save()

                for habit_info in user_info["habits"]:
                    Habit.objects.create(
                        user=user,
                        place=habit_info["place"],
                        time=habit_info["time"],
                        action=habit_info["action"],
                        is_reward=habit_info["is_reward"],
                        frequency=habit_info["frequency"],
                        reward=habit_info["reward"],
                        estimated_time=habit_info["estimated_time"],
                        is_public=habit_info["is_public"],
                        notification=habit_info["notification"],
                    )
        except Exception as e:
            print(e)
