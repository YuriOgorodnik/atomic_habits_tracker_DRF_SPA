from datetime import datetime, timedelta


def check_starting(habit, current_day):
    """
    Проверяет должна ли стартовать привычка сегодня или завтра (если условие выполняется,
    то устанавливается is_starting = True)
    """
    if not habit.is_starting:
        if habit.weekday == "today":
            habit.is_starting = True
        elif habit.weekday == "tomorrow" and current_day == habit.date_of_start.day + 1:
            habit.is_starting = True
        habit.save()


def check_frequency_weekly(habit):
    """
    Обновляет дату начала привычки в зависимости от периодичности её выполнения (ежедневно или еженедельно).
    """
    if habit.frequency == "weekly":
        habit.date_of_start += timedelta(days=7)
    else:
        habit.date_of_start += timedelta(days=1)
    habit.save()


def get_mailing_time(habit):
    """
    Возвращает день и время для отправки уведомления пользователю о необходимости выполнения привычки.
    """
    mailing_date = datetime.combine(habit.date_of_start, habit.time)

    if habit.notification_time == "fifteen":
        mailing_date -= timedelta(minutes=15)
    elif habit.notification_time == "thirty":
        mailing_date -= timedelta(minutes=30)
    elif habit.notification_time == "hour":
        mailing_date -= timedelta(hours=1)
    elif habit.notification_time == "two_hours":
        mailing_date -= timedelta(hours=2)
    else:
        mailing_date -= timedelta(days=1)

    return mailing_date.day, mailing_date.hour, mailing_date.minute
