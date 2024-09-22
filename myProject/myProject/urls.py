
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myProject.views import *
from myProject.AdminViews import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginPage,name="loginPage" ),
    path('signupPage/',signupPage,name="signupPage" ),
    path('JobFeed/',JobFeed,name="JobFeed" ),
    path('logoutPage/',logoutPage,name="logoutPage" ),
    path('addSkillPage/',addSkillPage,name="addSkillPage"),
    path('createBasicInfo/',createBasicInfo,name="createBasicInfo"),
    path('profilePage/',profilePage,name="profilePage"),
    path('addLanugage/',addLanugage,name="addLanugage"),
    path('MySettingsPage/',MySettingsPage,name="MySettingsPage"),
    path('LanguageEditbyUser/<str:myid>',LanguageEditbyUser,name="LanguageEditbyUser"),
    path('addSkillPage/',addSkillPage,name="addSkillPage"),
    path('skillEditByUser/<str:myid>',skillEditByUser,name="skillEditByUser"),
    path('add_education',add_education,name="add_education"),
    path('add_interest',add_interest,name="add_interest"),
    path('edit_education/<str:education_id>',edit_education,name="edit_education"),
    path('edit_interest/<str:interest_id>',edit_interest,name="edit_interest"),
    path('add-experience/', add_experience, name='add_experience'),
    path('edit_experience/<int:experience_id>/', edit_experience, name='edit_experience'),
    
    
    path('settings/', MySettingsPage, name='MySettingsPage'),
    path('editResumePage/', editResumePage, name='editResumePage'),
    path('view-full-resume/', viewFullResume, name='viewFullResume'),
    
    
    path('delete_language/<int:language_id>/', delete_language, name='delete_language'),
    path('delete_skill/<int:skill_id>/', delete_skill, name='delete_skill'),
    path('delete_interest/<int:interest_id>/', delete_interest, name='delete_interest'),
    path('delete_education/<int:education_id>/', delete_education, name='delete_education'),
    path('delete_experience/<int:experience_id>/', delete_experience, name='delete_experience'),
    
    
    path('view-add_job_Page/', add_job_Page, name='add_job_Page'),
    path('CreatedJob/', CreatedJob, name='CreatedJob'),
    
    path('jobs/edit/<int:job_id>/', edit_job_Page, name='edit_job'),
    path('jobs/delete/<int:job_id>/', delete_job, name='delete_job'),
     path('jobs/apply/<int:job_id>/', apply_job, name='apply_job'),
     path('profile/applied-jobs/', applied_jobs_list, name='applied_jobs_list'),
     path('search/', search_jobs, name='search_jobs'),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
