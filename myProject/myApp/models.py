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
    
    GENDER=[
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ]
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
    
    gender_type=models.CharField(max_length=200,null=True,choices=GENDER)

    def __str__(self):
        return f"Designation: {self.Designation} and Username: {self.user.username}"
    

class Education_model(models.Model):
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,null=True)
    start_year=models.DateField(null=True,max_length=100)
    end_year=models.DateField(null=True,max_length=100)
    
    def __str__(self) -> str:
        return f"{self.user.username}-{self.title}"
    
class Skill_model(models.Model):
    
    PROFIENCY=[
        ('high','High'),
        ('mideum','Mideum'),
        ('low','Low'),
    ]
    
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    Skill_Name=models.CharField(max_length=100,null=True)
    Proficiency_Level=models.CharField(max_length=100,null=True,choices=PROFIENCY)
    
    
    def __str__(self) -> str:
        return f"{self.user.username}-{self.Skill_Name}"
    
    
class Experience_Model(models.Model):
    
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    Title=models.CharField(max_length=100,null=True)
    Start_Date=models.DateField(max_length=100,null=True)
    End_Date=models.DateField(max_length=100,null=True)
    Description=models.TextField(max_length=100,null=True)
    
    
    def __str__(self) -> str:
        return f"{self.user.username}-{self.Title}"
    
class Interest_Model(models.Model):
    
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    
    Interest_Name=models.CharField(max_length=100,null=True)
    
    
    
    def __str__(self) -> str:
        return f"{self.user.username}-{self.Interest_Name}"
    
class Language_Model(models.Model):
    PROFIENCY=[
        ('high','High'),
        ('mideum','Mideum'),
        ('low','Low'),
    ]
    
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    language_name=models.CharField(max_length=100,null=True)
    Proficiency_Level=models.CharField(max_length=100,null=True,choices=PROFIENCY)
    
    
    def __str__(self) -> str:
        return f"{self.user.username}-{self.language_name}"
    
    
    
    