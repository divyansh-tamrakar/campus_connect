from django.http import JsonResponse
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework import status


from .serializers import UserCreateSerializer, DepartmentSerializer
from ..models import Department


@api_view(['GET'])
def getRoutes(request):
    urls = [
        'api/token', 
        'api/token/refresh'
        ]
    return Response(urls)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username

        return token
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
class Register(APIView):
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

@api_view(['GET'])
def get_all_departments(request):
    department = Department.objects.all()
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_department(request):
    data = request.data
    serializer = DepartmentSerializer(data=data, many=False)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def department_details(request, pk):
    department = Department.objects.get(id=pk)
    # users_in_department = department.user_set.all()
    department_serializer = DepartmentSerializer(department, many=False)
    users = department_serializer.get_users(pk)
    response = {
        'department': department_serializer.data,
        'users': users
    }
    return Response(response, status=status.HTTP_200_OK)