from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее только владельцу
    объекта выполнять определенные действия.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, имеет ли пользователь разрешение на выполнение
        определенного действия относительно данного объекта.
        """

        if request.method in permissions.SAFE_METHODS:
            # Если метод запроса является безопасным (GET), то разрешаем доступ.
            return True

        # Возвращаем True, если пользователь является владельцем объекта.
        return obj.user == request.user


class IsUser(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее только
    зарегистрированным пользователям выполнять определенные действия.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь разрешение на выполнение
        определенного действия.
        """
        if request.user.is_staff:
            # Если пользователь является администратором, разрешаем доступ.
            return True

        # Возвращаем True, если пользователь совпадает с объектом запроса.
        return request.user == view.get_object()
