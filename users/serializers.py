from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
            "phone",
            "city",
            "avatar",
            "chat_id",
        ]

    def save(self, *args, **kwargs):
        """
        Метод для сохранения пользователя.
        """
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        # Проверяем совпадение паролей
        if password != password2:
            # Если пароли не валидны, то возбуждаем ошибку
            raise serializers.ValidationError("Password doesn't match")

        # Cоздаем пользователя
        user = User.objects.create(
            email=self.validated_data.get("email"),
            phone=self.validated_data.get("phone"),
            city=self.validated_data.get("city", None),
            avatar=self.validated_data.get("avatar", None),
            chat_id=self.validated_data.get("chat_id"),
        )

        # Сохраняем пароль
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя (просмотр, изменение, удаление).
    """

    class Meta:
        model = User
        fields = ("email", "phone", "city", "avatar", "chat_id")
