from rest_framework import serializers

from django.contrib.auth import authenticate

from ..models import User, Department


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'department')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'department', 'name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if len(password) < 7:
            raise serializers.ValidationError("Password must be at least 7 characters")
        
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance
    

class DepartmentSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = ['id', 'name', 'users']
    
    def get_users(self, department_id):
        users = User.objects.filter(department=department_id)
        serializers = UserSerializer(users, many=True)
        return serializers.data