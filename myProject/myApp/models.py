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
    contact_No=models.CharField(max_length=100,null=True)
    Designation=models.CharField(max_length=100,null=True)
    Profile_Pic=models.ImageField(upload_to="Media/Profile_Pic",null=True)
    Carrer_Summary=models.CharField(max_length=100,null=True)
    Age=models.PositiveIntegerField(null=True)
    Gender=models.CharField(max_length=100,null=True)
    
    def __str__(self) -> str:
        return self.user.username+ " "+ self.Designation

    
class IntermediateLanguageModel(models.Model):
    
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    Language_Name=models.CharField(max_length=100,null=True)

    
    def __str__(self) -> str:
        return self.Language_Name  
    
class LanguageModel(models.Model):
    
    Proficiency_Level_Choices=[
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert'),
    ]

    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    Language_Name=models.CharField(max_length=100,null=True)
    Proficiency_Level=models.CharField(choices=Proficiency_Level_Choices,max_length=100,null=True)
    
    
    class Meta:
        unique_together=['user','Language_Name']
    
    def __str__(self) -> str:
        return self.user.username+ " "+ self.Language_Name
    
class IntermediateLanguageModel(models.Model):
    
    Language_Name=models.CharField(max_length=100,null=True)
    
    def __str__(self) -> str:
        return self.Language_Name
    
    
    
    
    
    
    
