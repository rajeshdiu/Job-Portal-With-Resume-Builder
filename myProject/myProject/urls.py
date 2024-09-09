
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
    path('addResumePage/',addResumePage,name="addResumePage" ),
    path('resumeList/',resumeList,name="resumeList" ),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
