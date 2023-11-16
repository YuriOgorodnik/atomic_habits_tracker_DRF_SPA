from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """
    Класс пагинации для списка привычек.
    """

    page_size = 5
