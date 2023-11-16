from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from permissions import IsUser
from users.models import User

from users.serializers import UserSerializer, UserRegisterSerializer


class UserListAPIView(generics.ListAPIView):
    """
    Представление для просмотра списка пользователей.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового пользователя.
    """

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения информации о пользователе.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser]


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления информации о пользователе.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUser]
