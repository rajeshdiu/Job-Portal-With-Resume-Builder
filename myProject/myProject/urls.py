
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',loginPage,name="loginPage" ),
    path('signupPage/',signupPage,name="signupPage" ),
    path('homePage/',homePage,name="homePage" ),
    path('logoutPage/',logoutPage,name="logoutPage" ),
    path('addSkillPage/',addSkillPage,name="addSkillPage"),
    path('addEducation/',addEducation,name="addEducation"),
    path('createResumePage/',createResumePage,name="createResumePage"),
    path('profilePage/',profilePage,name="profilePage"),
    path('addLanugage/',addLanugage,name="addLanugage"),
    path('LanguageListbyUser/',LanguageListbyUser,name="LanguageListbyUser"),
    path('LanguageEditbyUser/<str:myid>',LanguageEditbyUser,name="LanguageEditbyUser"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
