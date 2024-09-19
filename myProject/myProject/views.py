from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from myApp.models import *

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

def loginPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=authenticate(username=username,password=password)
        
        if user:
            login(request,user)
            return redirect("homePage")
        else:
            return HttpResponse("User Is not valid")
            
           
    return render(request,"loginPage.html")

def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        usertype=request.POST.get("usertype")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
        
        if password==confirm_password:
            
            user=CustomUser.objects.create_user(
                username=username,
                email=email,
                usertype=usertype,
                password=password
            )
            
            return redirect("loginPage")
        
    
    return render(request,"signupPage.html")


def logoutPage(request):
    
    logout(request)
    
    return redirect("loginPage")

@login_required
def homePage(request):
    
    return render(request,"homePage.html")


def addSkillPage(request):
    
    if request.user.usertype == 'admin':
        return render(request,"addSkillPage.html")
    else:
        return HttpResponse("You are not authorized to access this page")

def addEducation(request):
    
    if request.user.usertype == 'admin':
        return render(request,"addEducation.html")
    else:
        return HttpResponse("You are not authorized to access this page")
    
def createResumePage(request):
    if request.user.usertype == 'viewer':
        current_user=request.user
        if request.method=='POST':
            
            resume, created= ResumeModel.objects.get_or_create(user=current_user)
            
            resume.contact_No=request.POST.get("contact_No")
            resume.Designation=request.POST.get("Designation")
            resume.Profile_Pic=request.FILES.get("Profile_Pic")
            resume.Carrer_Summary=request.POST.get("Carrer_Summary")
            resume.Age=request.POST.get("Age")
            resume.Gender=request.POST.get("Gender")
            resume.save()
            current_user.first_name=request.POST.get("first_name")
            current_user.last_name=request.POST.get("second_name")
            
            current_user.save()

        return render(request,"createResumePage.html")
    else:
        return HttpResponse("You are not authorized to access this page")
    
def profilePage(request):
    current_user = request.user

    information = get_object_or_404(ResumeModel, user=current_user)
    Language = LanguageModel.objects.filter(user=current_user)

    context = {
        'Information': information,
        'Language': Language
    }
    
    return render(request, "profilePage.html", context)


def addLanugage(request):
    all_lan = IntermediateLanguageModel.objects.all()
    
    if request.user.usertype == 'viewer':
        current_user = request.user
        
        if request.method == 'POST':
            Language_Id = request.POST.get("Language_Id")
            Proficiency_Level = request.POST.get("Proficiency_Level")
            
            Language_Object = get_object_or_404(IntermediateLanguageModel, id=Language_Id)
            
            if LanguageModel.objects.filter(user=current_user, Language_Name=Language_Object.Language_Name).exists():
                return HttpResponse("Already Exist")
            
            resume = LanguageModel(
                user=current_user,
                Language_Name=Language_Object.Language_Name,  
                Proficiency_Level=Proficiency_Level,
            )
            resume.save()
    
    context = {
        "all_lan": all_lan
    }
    
    return render(request, "addLanugage.html", context)


def LanguageListbyUser(request):
    
    current_user=request.user
    
    myLanguage=LanguageModel.objects.filter(user=current_user)
    context={
        "myLanguage":myLanguage
    }
    
    return render(request,"LanguageListbyUser.html",context)

def LanguageEditbyUser(request, myid):
    all_lan = IntermediateLanguageModel.objects.all()
    myLanguage = LanguageModel.objects.get(id=myid)
    
    if request.user.usertype == 'viewer':
        current_user = request.user
        
        if request.method == 'POST':
            Language_Id = request.POST.get("Language_Id")
            Proficiency_Level = request.POST.get("Proficiency_Level")
            
            Language_Object = get_object_or_404(IntermediateLanguageModel, id=Language_Id)
            
            resume = LanguageModel(
                id=myid,
                user=current_user,
                Language_Name=Language_Object.Language_Name,
                Proficiency_Level=Proficiency_Level,
            )
            resume.save()
    
    context = {
        "myLanguage": myLanguage,
        "all_lan": all_lan
    }
    
    return render(request, "LanguageEditbyUser.html", context)

