from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.relations import PrimaryKeyRelatedField

from files.models import File

User = get_user_model()


class FileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_username', 'title', 'file', 'updated_time')


class FileCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ('title', 'file')

    def create(self, user, validated_data):
        return File.objects.create(
            user=user,
            **validated_data
        )


