from typing import OrderedDict

from rest_framework import serializers

from ...models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title"
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "second_name", "group")


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "second_name", "password", "group")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data) -> User:
        return User.objects.create_user(**validated_data)

    @property
    def data(self) -> OrderedDict:
        """
        It's make for returning title of group instead id after user creation.
        """
        return UserRetrieveSerializer(instance=self.instance).data
