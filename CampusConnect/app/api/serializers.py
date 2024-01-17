from rest_framework import serializers

from django.contrib.auth import authenticate

from ..models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
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
    
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(self.context.get('request'), username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Incorrect Credentials", 400)
            
            if not user.is_active:
                raise serializers.ValidationError('No active user found', 400)
            
            return user
        else:
            raise serializers.ValidationError({'detail':'Must provide both username and password.'}, 400)