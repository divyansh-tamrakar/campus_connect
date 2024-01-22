from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class Department(models.Model):
    
    """
     Model to Create different Departments in the college 
    """
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.username    
    
    
class Hod(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE)