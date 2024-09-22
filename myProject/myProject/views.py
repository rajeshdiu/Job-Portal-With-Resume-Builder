from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404

from django.db.models import Q 


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.warning(request, "Both username and password are required")
            return render(request, "loginPage.html")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect("JobFeed")
        else:
            messages.warning(request, "Invalid username or password")

    return render(request, "loginPage.html")


def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        usertype = request.POST.get("usertype")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([username, email, usertype, password, confirm_password]):
            messages.warning(request, "All fields are required")
            return render(request, "signupPage.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format")
            return render(request, "signupPage.html")

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, "signupPage.html")

        if len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters long")
            return render(request, "signupPage.html")

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(request, "Password must contain both letters and numbers")
            return render(request, "signupPage.html")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                usertype=usertype,
                password=password
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("loginPage")
        except IntegrityError:
            messages.warning(request, "Username or email already exists")
            return render(request, "signupPage.html")

    return render(request, "signupPage.html")


def logoutPage(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("loginPage")


@login_required
def JobFeed(request):
    jobs = AddJobModel.objects.all()  # Fetch all jobs
    applied_jobs = JobApplication.objects.filter(user=request.user).values_list('job_id', flat=True)  # Get IDs of jobs the user has applied to

    context = {
        'jobs': jobs,
        'applied_jobs': applied_jobs,  # Pass the list of applied job IDs to the template
    }

    return render(request, 'JobFeed.html', context)




def search_jobs(request):
    query = request.GET.get('query')  # Get the search query from the GET request
    if query:
        # Use Q objects to search across multiple fields
        jobs = AddJobModel.objects.filter(
            Q(job_title__icontains=query) |
            Q(description__icontains=query) |
            Q(company_name__icontains=query)
        )
    else:
        jobs = AddJobModel.objects.none()  # Return no jobs if no query is provided

    return render(request, 'search.html', {'jobs': jobs, 'query': query})



@login_required
def apply_job(request, job_id):
    job = get_object_or_404(AddJobModel, id=job_id)
    application_exists = JobApplication.objects.filter(job=job, user=request.user).exists()

    if request.method == "POST":
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter')

        if resume and cover_letter:
            application = JobApplication(
                job=job,
                user=request.user,
                resume=resume,
                cover_letter=cover_letter
            )
            application.save()
            messages.success(request, f"You have successfully applied for {job.title}!")
            return redirect('job_feed')
        else:
            messages.error(request, "Please upload a resume and enter a cover letter.")

    return render(request, "apply_job.html", {"job": job, "application_exists": application_exists})

def applied_jobs_list(request):
    applied_jobs = JobApplication.objects.filter(user=request.user)  # Fetch all jobs applied by the current user
    return render(request, 'applied_jobs_list.html', {'applied_jobs': applied_jobs})

@login_required
def createBasicInfo(request):
    if request.user.usertype == 'viewer' or request.user.usertype == 'admin' :
        current_user = request.user
        
        if request.method == 'POST':
            resume, created = BasicInfoModel.objects.get_or_create(user=current_user)
            
            resume.contact_No = request.POST.get("contact_No")
            resume.Designation = request.POST.get("Designation")
            resume.Profile_Pic = request.FILES.get("Profile_Pic")
            resume.Carrer_Summary = request.POST.get("Carrer_Summary")
            resume.Age = request.POST.get("Age")
            resume.Gender = request.POST.get("Gender")
            resume.save()
            
            current_user.first_name = request.POST.get("first_name")
            current_user.last_name = request.POST.get("second_name")
            current_user.save()
            
            messages.success(request, "Resume created successfully.")
            return redirect('MySettingsPage')  
        
        return render(request, "createBasicInfo.html")
    elif request.user.usertype == 'admin':
        messages.warning(request, "You are not authorized to access this page.")
        return render(request, "createBasicInfo.html") 
    

@login_required
def viewFullResume(request):
    current_user = request.user

    # Fetch the user's resume information
    information = get_object_or_404(BasicInfoModel, user=current_user)
    languages = LanguageModel.objects.filter(user=current_user)
    skills = SkillModel.objects.filter(user=current_user)
    education = EducationModel.objects.filter(user=current_user)
    interests = InterestModel.objects.filter(user=current_user)
    experiences = ExperienceModel.objects.filter(user=current_user)

    # Fetching additional user information
    user_info = {
        'username': current_user.username,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
    }

    context = {
        'Information': information,
        'Languages': languages,
        'Skills': skills,
        'Education': education,
        'Interests': interests,
        'Experiences': experiences,
        'UserInfo': user_info, 
    }

    return render(request, "fullResumePage.html", context)




@login_required
def editResumePage(request):
    current_user = request.user
    information = get_object_or_404(BasicInfoModel, user=current_user)

    if request.method == 'POST':
        designation = request.POST.get('Designation')
        age = request.POST.get('Age')
        gender = request.POST.get('Gender')
        career_summary = request.POST.get('Carrer_Summary')
        contact_no = request.POST.get('contact_No')
        profile_pic = request.FILES.get('Profile_Pic')

        # Validate the form data
        if not designation or not age or not gender:
            messages.error(request, "Please fill in all required fields.")
        else:
            # Update the information
            information.Designation = designation
            information.Age = age
            information.Gender = gender
            information.Carrer_Summary = career_summary
            information.contact_No = contact_no
            if profile_pic:
                information.Profile_Pic = profile_pic

            information.save()
            messages.success(request, 'Resume updated successfully!')
            return redirect('profilePage')

    context = {
        'Information': information
    }

    return render(request, "editResumePage.html", context)

    

@login_required
def MySettingsPage(request):
    
    current_user=request.user
    
    myLanguage=LanguageModel.objects.filter(user=current_user)
    mySkill=SkillModel.objects.filter(user=current_user)
    myEducation=EducationModel.objects.filter(user=current_user)
    myInterest=InterestModel.objects.filter(user=current_user)
    myExperience=ExperienceModel.objects.filter(user=current_user)
    
    context={
        "myLanguage":myLanguage,
        "mySkill":mySkill,
        "myInterest":myInterest,
        'myEducation':myEducation,
        "myExperience":myExperience
    }
    
    return render(request,"MySettingsPage.html",context)


@login_required
def profilePage(request):
    current_user = request.user

    try:
        information = get_object_or_404(BasicInfoModel, user=current_user)
    except Http404:
        messages.warning(request, "You don't have a resume. Please create one.")
        return redirect('createBasicInfo') 

    languages = LanguageModel.objects.filter(user=current_user)
    skills = SkillModel.objects.filter(user=current_user)
    education = EducationModel.objects.filter(user=current_user)
    interests = InterestModel.objects.filter(user=current_user)
    experiences = ExperienceModel.objects.filter(user=current_user)

    context = {
        'Information': information,
        'Languages': languages,
        'Skills': skills,
        'Education': education,
        'Interests': interests,
        'Experiences': experiences,
    }
    
    return render(request, "profilePage.html", context)


@login_required
def add_education(request):
    # Check if the user is a viewer
    if request.user.usertype != 'viewer':
        messages.warning(request, "You are not authorized to add education information.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    institutes = InstituteNameModel.objects.all()  # Get all institutes
    degrees = DegreeModel.objects.all()  # Get all degrees
    fields_of_study = FieldOfStudyModel.objects.all()  # Get all fields of study

    if request.method == 'POST':
        institution_name = request.POST.get('institution_name')
        degree_name = request.POST.get('degree_name')
        field_of_study_name = request.POST.get('field_of_study')  # Get field of study from dropdown
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Create and save the new education entry
        EducationModel.objects.create(
            user=request.user,  # Assuming the user is logged in
            institution_name=institution_name,
            degree=degree_name,
            field_of_study=field_of_study_name,
            start_date=start_date,
            end_date=end_date
        )
        messages.success(request, "Education added successfully.")
        return redirect('MySettingsPage')  # Redirect to a success page or another view

    return render(request, 'add_education.html', {
        'institutes': institutes,
        'degrees': degrees,
        'fields_of_study': fields_of_study
    })


@login_required
def add_interest(request):
    # Check if the user is a viewer
    if request.user.usertype != 'viewer':
        messages.warning(request, "You are not authorized to add interests.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate the input
        if not name or not description:
            messages.warning(request, "Both name and description are required.")
            return render(request, 'add_interest.html')

        InterestModel.objects.create(
            user=request.user, 
            name=name,
            description=description
        )
        messages.success(request, "Interest added successfully.")
        return redirect('MySettingsPage')

    return render(request, 'add_interest.html')

@login_required
def addLanugage(request):
    # Check if the user is a viewer
    if request.user.usertype != 'viewer':
        messages.warning(request, "You are not authorized to add languages.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    all_lan = IntermediateLanguageModel.objects.all()
    current_user = request.user

    if request.method == 'POST':
        Language_Id = request.POST.get("Language_Id")
        Proficiency_Level = request.POST.get("Proficiency_Level")

        # Validate the input
        if not Language_Id or not Proficiency_Level:
            messages.warning(request, "Both language and proficiency level are required.")
            return render(request, "addLanugage.html", {'all_lan': all_lan})

        MyObj = get_object_or_404(IntermediateLanguageModel, id=Language_Id)

        if LanguageModel.objects.filter(user=current_user, Language_Name=MyObj.Language_Name).exists():
            messages.warning(request, "This language already exists in your profile.")
            return render(request, "addLanugage.html", {'all_lan': all_lan})

        LanguageModel.objects.create(
            user=current_user,
            Language_Name=MyObj.Language_Name,
            Proficiency_Level=Proficiency_Level,
        )
        messages.success(request, "Language added successfully.")
        return redirect("MySettingsPage")

    context = {
        "all_lan": all_lan
    }
    return render(request, "addLanugage.html", context)

@login_required
def add_experience(request):
    # Check if the user is a viewer
    if request.user.usertype != 'viewer':
        messages.warning(request, "You are not authorized to add experience.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        # Validate the input
        if not job_title or not company_name or not start_date:
            messages.warning(request, "Job title, company name, and start date are required.")
            return render(request, 'add_experience.html')

        # Create and save the new experience entry
        ExperienceModel.objects.create(
            user=request.user,
            job_title=job_title,
            company_name=company_name,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        messages.success(request, "Experience added successfully.")
        return redirect('MySettingsPage')  # Redirect to your desired URL

    return render(request, 'add_experience.html')

@login_required
def addSkillPage(request):
    # Check if the user is a viewer
    if request.user.usertype != 'viewer':
        messages.warning(request, "You are not authorized to add skills.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    All_Skill = IntermediateSkillModel.objects.all()
    current_user = request.user

    if request.method == 'POST':
        Skill_Id = request.POST.get("Skill_Id")
        Skill_Level = request.POST.get("Skill_Level")

        MyObj = get_object_or_404(IntermediateSkillModel, id=Skill_Id)

        # Check if the skill already exists for the user
        if SkillModel.objects.filter(user=current_user, Skill_Name=MyObj.My_Skill_Name).exists():
            messages.warning(request, "Skill already exists.")
        else:
            skill = SkillModel(
                user=current_user,
                Skill_Name=MyObj.My_Skill_Name,
                Skill_Level=Skill_Level,
            )
            skill.save()
            messages.success(request, "Skill added successfully.")
            return redirect("MySettingsPage")

    context = {
        "All_Skill": All_Skill
    }

    return render(request, "addSkillPage.html", context)


@login_required
def edit_education(request, education_id):
    education = get_object_or_404(EducationModel, id=education_id)
    institutes = InstituteNameModel.objects.all() 
    degrees = DegreeModel.objects.all() 
    fields_of_study = FieldOfStudyModel.objects.all() 

    # Authorization check
    if request.user != education.user and request.user.usertype != 'admin':
        messages.warning(request, "You are not authorized to edit this education entry.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        education.institution_name = request.POST.get('institution_name')
        education.degree = request.POST.get('degree_name')
        education.field_of_study = request.POST.get('field_of_study')
        education.start_date = request.POST.get('start_date')
        education.end_date = request.POST.get('end_date')

        education.save()
        messages.success(request, "Education entry updated successfully.")
        return redirect('MySettingsPage') 
    
    context = {
        'education': education,
        'institutes': institutes,
        'degrees': degrees,
        'fields_of_study': fields_of_study
    }

    return render(request, 'edit_education.html', context)


@login_required
def edit_interest(request, interest_id):
    interest = get_object_or_404(InterestModel, id=interest_id)

    # Authorization check
    if request.user != interest.user and request.user.usertype != 'admin':
        messages.warning(request, "You are not authorized to edit this interest.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        interest.name = request.POST.get('name')
        interest.description = request.POST.get('description')
        interest.save()
        messages.success(request, "Interest updated successfully.")
        return redirect('MySettingsPage')  # Redirect to success page

    return render(request, 'edit_interest.html', {
        'interest': interest
    })

@login_required
def edit_experience(request, experience_id):
    experience = get_object_or_404(ExperienceModel, id=experience_id)

    # Authorization check
    if request.user != experience.user and request.user.usertype != 'admin':
        messages.warning(request, "You are not authorized to edit this experience.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    context = {
        'experience': experience
    }

    if request.method == 'POST':
        experience.job_title = request.POST.get('job_title')
        experience.company_name = request.POST.get('company_name')
        experience.start_date = request.POST.get('start_date')
        experience.end_date = request.POST.get('end_date')
        experience.description = request.POST.get('description')
        experience.save()
        
        messages.success(request, "Experience updated successfully.")
        return redirect('MySettingsPage')  # Redirect to the settings page after successful update

    return render(request, 'edit_experience.html', context)
@login_required
def LanguageEditbyUser(request, myid):
    all_lan = IntermediateLanguageModel.objects.all()
    myLanguage = get_object_or_404(LanguageModel, id=myid)

    # Authorization check
    if request.user.usertype != 'viewer':
        messages.warning(request, "You are not authorized to edit this language.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        Language_Id = request.POST.get("Language_Id")
        Proficiency_Level = request.POST.get("Proficiency_Level")

        Language_Object = get_object_or_404(IntermediateLanguageModel, id=Language_Id)

        myLanguage.Language_Name = Language_Object.Language_Name
        myLanguage.Proficiency_Level = Proficiency_Level
        myLanguage.save()

        messages.success(request, "Language updated successfully.")
        return redirect("MySettingsPage")

    context = {
        "myLanguage": myLanguage,
        "all_lan": all_lan
    }

    return render(request, "LanguageEditbyUser.html", context)

@login_required
def skillEditByUser(request, myid):
    MY_Skill = get_object_or_404(SkillModel, id=myid)
    ALL_Skill = IntermediateSkillModel.objects.all()
    current_user = request.user

    # Authorization check
    if MY_Skill.user != current_user:
        messages.warning(request, "You are not authorized to edit this skill.")
        return redirect("MySettingsPage")  # Redirect to an appropriate page

    if request.method == 'POST':
        Skill_Id = request.POST.get("Skill_Id")
        Skill_Level = request.POST.get("Skill_Level")

        MyObj = get_object_or_404(IntermediateSkillModel, id=Skill_Id)

        # Update existing skill instead of creating a new one
        MY_Skill.Skill_Name = MyObj.My_Skill_Name
        MY_Skill.Skill_Level = Skill_Level
        MY_Skill.save()

        messages.success(request, "Skill updated successfully.")
        return redirect("MySettingsPage")

    context = {
        "MY_Skill": MY_Skill,
        "ALL_Skill": ALL_Skill,
        "Proficiency_Level_Choices": SkillModel.Skill_Level_Choices
    }

    return render(request, "skillEditByUser.html", context)

@login_required
def delete_language(request, language_id):
    language = get_object_or_404(LanguageModel, id=language_id, user=request.user)
    language.delete()
    messages.success(request, 'Language deleted successfully.')
    return redirect('MySettingsPage')

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(SkillModel, id=skill_id, user=request.user)
    skill.delete()
    messages.success(request, 'Skill deleted successfully.')
    return redirect('MySettingsPage')

@login_required
def delete_interest(request, interest_id):
    interest = get_object_or_404(InterestModel, id=interest_id, user=request.user)
    interest.delete()
    messages.success(request, 'Interest deleted successfully.')
    return redirect('MySettingsPage')

@login_required
def delete_education(request, education_id):
    education = get_object_or_404(EducationModel, id=education_id, user=request.user)
    education.delete()
    messages.success(request, 'Education deleted successfully.')
    return redirect('MySettingsPage')

@login_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(ExperienceModel, id=experience_id, user=request.user)
    experience.delete()
    messages.success(request, 'Experience deleted successfully.')
    return redirect('MySettingsPage')



    