from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    USER=[
        ('admin','Admin'),
        ('viewer','Viewer')
    ]
    usertype=models.CharField(choices=USER,null=True,max_length=100)
    
    def __str__(self):
        return f"{self.username}- {self.first_name}- {self.last_name}"
    
class ResumeModel(models.Model):
    user=models.OneToOneField(CustomUser,null=True,on_delete=models.CASCADE)
    Designation=models.CharField(max_length=100,null=True)
    Contact_Number=models.CharField(max_length=100,null=True)
    Carrer_Summary=models.TextField(max_length=100,null=True)
    Experience_Title=models.CharField(max_length=100,null=True)
    Skill_Title=models.CharField(max_length=100,null=True)
    Education_Title=models.CharField(max_length=100,null=True)
    Language=models.CharField(max_length=100,null=True)
    Interest=models.CharField(max_length=100,null=True)
    Profile_pic=models.ImageField(upload_to="Media/Profile_Pic",null=True)
    Linkedin_URL=models.URLField(max_length=200,null=True)
    Facebook_URL=models.URLField(max_length=200,null=True)
    Instagram_URL=models.URLField(max_length=200,null=True)
    GitHub_URL=models.URLField(max_length=200,null=True)

    def __str__(self):
        return f"Designation: {self.Designation} and Username: {self.user.username}"
    