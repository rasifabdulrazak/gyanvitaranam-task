from django.shortcuts import render
from rest_framework import viewsets, generics, views
from .models import Company, Employee, ProfilePic
from .serializer import (
    CompanySerializer,
    EmployeeSerializer,
    ProfileSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
)
from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget
from django import forms


User = get_user_model()


# Create your views here.


class ComapanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.order_by("-id")
    serializer_class = CompanySerializer
    search_fields = {
        "company_name",
        "company_id",
        "short_code",
    }


class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.order_by("-id")
    serializer_class = EmployeeSerializer
    search_fields = {
        "employee_name",
        "employee_id",
    }


class ProfileView(generics.ListCreateAPIView):
    queryset = ProfilePic.objects.all()
    parser_classes = {FormParser, MultiPartParser}
    serializer_class = ProfileSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserLoginView(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]
    authentication_classes = [TokenAuthentication]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            # Authenticate user
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                # User authenticated, generate token
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "token": token.key,
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                    }
                )
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

