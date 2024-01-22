from django.urls import path

from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.getRoutes),
    
    path('departments/create', views.create_department,),
    path('departments/', views.get_all_departments),
    path('departments/<int:pk>', views.department_details),
    
    path("register", views.Register.as_view(), name="register_user"),
    
    
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token_view')

]
