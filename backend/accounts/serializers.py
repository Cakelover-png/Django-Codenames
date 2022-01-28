from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'password': _('პაროლის ფილდები არ დაემთხვა'),
                'confirm_password': _('პაროლის ფილდები არ დაემთხვა'),
            })
        return attrs

    def create(self, validated_data) -> 'User':
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)
