from django.contrib.auth import get_user_model

from rest_framework import generics, status, response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404


from .serializer import (
    UserAccountSerializer,
    UserAccountLoginSerializer,
    PrivateUserProfile,
)

from .utils import get_tokens_for_user, TokenHelper

User = get_user_model()


# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [AllowAny]


class UserLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserAccountLoginSerializer

    def post(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return response.Response(status=status.HTTP_200_OK, data=data.data)

    # Alternative way
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     tokens = TokenHelper().create_token(serializer.validated_data["user"])
    #     # validated_data["refresh"] = tokens["refresh"]
    #     # validated_data["access"] = tokens["access"]

    #     data = {
    #         "refresh": tokens[0],
    #         "access": tokens[1],
    #     }
    #     return response.Response(status=status.HTTP_200_OK, data=data)


class PrivateUserprofile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateUserProfile

    def get_object(self):
        return get_object_or_404(User, email=self.request.user.email)
