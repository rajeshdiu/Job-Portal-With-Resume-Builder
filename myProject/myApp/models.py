from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    
    USER=[
        ('admin','Admin'),
        ('viewer','Viewer')
    ]
    
    usertype=models.CharField(choices=USER,null=True,max_length=100)
    
    def __str__(self):
        return f"{self.username}- {self.first_name}- {self.last_name}"
    
    

class BasicInfoModel(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    contact_No = models.CharField(max_length=100, null=True)
    Designation = models.CharField(max_length=100, null=True)
    Profile_Pic = models.ImageField(upload_to="Media/Profile_Pic", null=True)
    Carrer_Summary = models.CharField(max_length=100, null=True)
    Age = models.PositiveIntegerField(null=True)
    Gender = models.CharField(max_length=100, null=True)
    
    # Date fields
    date_of_birth = models.DateField(null=True, blank=True)
 
    def __str__(self) -> str:
        return self.user.username + " " + self.Designation



class ExperienceModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.user.username})"


class InterestModel(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FieldOfStudyModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DegreeModel(models.Model):
    
    Degree=[
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctorate', 'Doctorate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=50, choices=Degree)

    def __str__(self):
        return self.name


class InstituteNameModel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    

class EducationModel(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=100, null=True)
    field_of_study = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'institution_name', 'degree']

    def __str__(self) -> str:
        return f"{self.user.username} - {self.institution_name} ({self.degree})"



    
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

    

class SkillModel(models.Model):
    
    
    Skill_Level_Choices=[
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert'),
    ]
    user=models.ForeignKey(CustomUser,null=True,on_delete=models.CASCADE)
    Skill_Name=models.CharField(max_length=100,null=True)
    Skill_Level=models.CharField(choices=Skill_Level_Choices,max_length=100,null=True)
    
    class Meta:
        unique_together=['user','Skill_Name']
    
    def __str__(self) -> str:
        return self.user.username+ " "+ self.Skill_Name
    
class IntermediateSkillModel(models.Model):
    
    My_Skill_Name=models.CharField(max_length=100,null=True)
    
    def __str__(self) -> str:
        return self.My_Skill_Name
    
    
class AddJobModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Job created by which user
    job_title = models.CharField(max_length=255,null=True)
    company_name = models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    requirements = models.TextField(null=True)
    salary = models.CharField(max_length=255,null=True)
    posted_on = models.DateField(default=timezone.now,null=True)
    updated_on = models.DateField(auto_now=True,null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.user.username})"
    
class JobApplication(models.Model):
    job = models.ForeignKey(AddJobModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} applied for {self.job.job_title}"
    
