from rest_framework import serializers
from .models import Company,Employee,ProfilePic
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        # fields = '__all__'
        exclude = ('is_deleted',)
        read_only_fields = ('is_active', 'is_deleted')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('is_deleted',)
        read_only_fields = ('is_active', 'is_deleted')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company_id'] = CompanySerializer(instance.company_id).data
        return response
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        exclude = ('is_deleted','is_active')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')

    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()