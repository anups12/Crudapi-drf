from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class Creator(models.Model):
    name= models.CharField(max_length=100)
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class Reader(models.Model):
    name= models.CharField(max_length=100)
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name
    

class Course(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(default= 'avatar.png', upload_to='images')
    description= models.TextField( null=True)
    user = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Enrolled(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Reader, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name
    
    
    def UserEnrolled(self):
        users = self.user_set.all()
        return users
    
    