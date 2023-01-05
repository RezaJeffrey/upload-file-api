from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, UserRegisterSerializer,
    UserUpdateSerializer, ChangeUserPasswordSerializer
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    # TODO [test] check permissions in tests

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action in ('partial_update', 'update'):
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangeUserPasswordSerializer

        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.pk)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(**serializer.validated_data)
            response = {
                "data": UserSerializer(serializer.data).data
            }
            code = status.HTTP_201_CREATED
        else:
            response = {
                "errors": serializer.errors
            }
            code = status.HTTP_400_BAD_REQUEST
        return Response(
            data=response,
            status=code
        )

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=user,
            validated_data=serializer.validated_data
        )
        response = {
            'message': 'password changed'
        }
        return Response(
            data=response,
            status=status.HTTP_201_CREATED
        )
