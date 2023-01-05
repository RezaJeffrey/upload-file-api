from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from files.models import File
from .serializers import FileDetailSerializer, FileCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class FileViewSet(ModelViewSet):

    def get_permissions(self):
        permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ return files of each user, admin can see all files """
        user = self.request.user
        if user.is_superuser:
            return File.objects.all()
        else:
            return File.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return FileCreateSerializer
        return FileDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(
            user=request.user,
            validated_data=serializer.validated_data
        )
        title = serializer.validated_data.get('title')
        content_type = request.FILES.get('file').content_type
        response = {
            'title': title,
            'type': content_type
        }
        code = status.HTTP_201_CREATED
        return Response(
            data=response,
            status=code
        )
