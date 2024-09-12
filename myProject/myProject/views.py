from django.shortcuts import render,redirect,get_object_or_404
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


def addResumePage(request):
    
    All_User=CustomUser.objects.all()
    
    if request.method=='POST':
        
        my_id=request.POST.get("all_user_name")
        
        
        Gender=request.POST.get("Gender")
        
        designation=request.POST.get("designation")
        contact_number=request.POST.get("contact_number")
        career_summary=request.POST.get("career_summary")
        experience_title=request.POST.get("experience_title")
        skill_title=request.POST.get("skill_title")
        education_title=request.POST.get("education_title")
        language=request.POST.get("language")
        interest=request.POST.get("interest")
        
        profile_pic=request.FILES.get("profile_pic")
        linkedin_url=request.POST.get("linkedin_url")
        facebook_url=request.POST.get("facebook_url")
        instagram_url=request.POST.get("instagram_url")
        github_url=request.POST.get("github_url")
        
        my_user=CustomUser.objects.get(id=my_id)
        
        resume=ResumeModel(
            user=my_user,
            Designation=designation,
            Contact_Number=contact_number,
            Carrer_Summary=career_summary,
            Experience_Title=experience_title,
            Skill_Title=skill_title,
            Education_Title=education_title,
            Language=language,
            Interest=interest,
            Profile_pic=profile_pic,
            Linkedin_URL=linkedin_url,
            Facebook_URL=facebook_url,
            Instagram_URL=instagram_url,
            GitHub_URL=github_url,
            gender_type=Gender,
        )
        
        resume.save()
        
        return redirect("resumeList")
    
    return render(request,"addResumePage.html",{'All_User':All_User})


def resumeList(request):
    data=ResumeModel.objects.all()
    
    context={
        'data':data
    }

    return render(request,"resumeList.html",context)


def editResume(request,myid):

    All_User=CustomUser.objects.all()
    data=ResumeModel.objects.get(id=myid)
    if request.method=='POST':
        my_id=request.POST.get("all_user_name")
        myid=request.POST.get("id")
        Gender=request.POST.get("Gender")
        designation=request.POST.get("designation")
        contact_number=request.POST.get("contact_number")
        career_summary=request.POST.get("career_summary")
        experience_title=request.POST.get("experience_title")
        skill_title=request.POST.get("skill_title")
        education_title=request.POST.get("education_title")
        language=request.POST.get("language")
        interest=request.POST.get("interest")
        profile_pic=request.FILES.get("profile_pic")
        linkedin_url=request.POST.get("linkedin_url")
        facebook_url=request.POST.get("facebook_url")
        instagram_url=request.POST.get("instagram_url")
        github_url=request.POST.get("github_url")
        my_user=CustomUser.objects.get(id=my_id)
        old_pic=request.POST.get("old_pic")
        resume=ResumeModel(
            id=my_id,
            user=my_user,
            Designation=designation,
            Contact_Number=contact_number,
            Carrer_Summary=career_summary,
            Experience_Title=experience_title,
            Skill_Title=skill_title,
            Education_Title=education_title,
            Language=language,
            Interest=interest,
            Linkedin_URL=linkedin_url,
            Facebook_URL=facebook_url,
            Instagram_URL=instagram_url,
            GitHub_URL=github_url,
            gender_type=Gender,
        )
        
        if profile_pic:
            resume.Profile_pic=profile_pic
            resume.save()
        else:
            
            resume.Profile_pic=old_pic
            resume.save()
            
        resume.save()
        
        return redirect("resumeList")

    context={
        "All_User":All_User,
        'data':data
    }
    
    return render(request,"editResume.html",context)


def viewResume(request,myid):
    
    my_user=get_object_or_404(CustomUser,id=myid)
    
    resume=ResumeModel.objects.filter(user=my_user)
    Education=Education_model.objects.filter(user=my_user)
    Skill=Skill_model.objects.filter(user=my_user)
    Experience=Experience_Model.objects.filter(user=my_user)
    Interest=Interest_Model.objects.filter(user=my_user)
    Language=Language_Model.objects.filter(user=my_user)
    
    context={
        'resume':resume,
        'Education':Education,
        'Skill':Skill,
        'Experience':Experience,
        'Interest':Interest,
        'Language':Language
    }
    
    return render(request,"viewResume.html",context)


def deleteResume(request,myid):
    
    data=ResumeModel.objects.get(id=myid).delete()
    
    return redirect("resumeList")
    