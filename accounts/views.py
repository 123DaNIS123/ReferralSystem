from django.contrib import auth
from django.utils import timezone

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from .serializers import UserAuthSerializer, UserProfileSerializer
from .models import CustomUser

import time

class AuthorizationView(GenericAPIView):
    permission_classes = []
    serializer_class = UserAuthSerializer
    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.user.is_authenticated)
        print(request.user)
        data = request.data
        serializer = UserAuthSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.filter(phone_number=data["phone_number"]).first()
        if not user:
            user = serializer.save()
            time.sleep(1)
            return Response({
                "message": "User created",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        if user.otp_valid_until < timezone.now():
            serializer = UserAuthSerializer(data = data, instance = user)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            time.sleep(1)
            return Response({
                "message": "User updated - password updated",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        if "password" in data:
            serializer = UserAuthSerializer(data = data, instance = user)
            serializer.is_valid(raise_exception=True)
            serializer.is_password_valid(serializer.validated_data, raise_exception=True)
            auth.login(request, user)
            return Response({"message": "Successfully authenticated",
                             "data": serializer.data,
                             }, status.HTTP_200_OK)
        return Response({
            "message": "Write a password"
        }, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        print(request.user.is_authenticated)
        queryset = CustomUser.objects.filter(invited_by=request.user)
        user = CustomUser.objects.get(pk=request.user.pk)
        serializer = UserProfileSerializer(instance=user)
        my_invites_list = list(map(lambda x: str(x), queryset))
        my_invites_str = ";".join(my_invites_list)
        return Response({
                "data": serializer.data,
                "my_invites": my_invites_str 
            }, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        print(request.user.is_authenticated)

        user = CustomUser.objects.filter(invitation_code=request.data["invited_by"]).first()
        if user:
            if request.user.pk != user.pk:
                request.user.invited_by = user
                request.user.save()
                return Response({"message": "Invite code added"},
                                status=status.HTTP_200_OK)
            return Response({"message": "Can't be referred by self"},
                        status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "No user with this invite code"},
                        status=status.HTTP_400_BAD_REQUEST)
    


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
        # request.user.auth_token.delete()
        return Response({"message": "User logged out"},status=status.HTTP_200_OK)

        
