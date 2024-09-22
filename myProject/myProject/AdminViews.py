from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from myApp.models import *
from django.contrib import messages

@login_required
def add_job_Page(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        job_description = request.POST.get('description')  # Ensure this matches the model's field name
        location = request.POST.get('location')
        requirements = request.POST.get('requirements')
        salary = request.POST.get('salary')

        # Validation check
        if not job_title or not company_name or not job_description or not location:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'myAdmin/add_job.html')

        # Create job entry in the database
        AddJob = AddJobModel(
            user=request.user,
            job_title=job_title,
            company_name=company_name,
            description=job_description,
            location=location,
            requirements=requirements,
            salary=salary,  # Ensure this matches the model's field name
        )
        AddJob.save()
        messages.success(request, 'Job created successfully.')
        return redirect('CreatedJob')  # Redirect to a page that lists all jobs created by the user

    return render(request, 'myAdmin/add_job.html')


def CreatedJob(request):
    # Check if the user is an admin
    if request.user.usertype == 'admin':
        # Get all the jobs created by users
        jobs = AddJobModel.objects.all()
        
        context = {
            'jobs': jobs,
        }
        
        return render(request, "myAdmin/CreatedJob.html", context)
    else:
        messages.warning(request, "You are not authorized to view this page.")
        return redirect('homePage')
    

@login_required
def edit_job_Page(request, job_id):
    # Retrieve the job instance or return a 404 error if it doesn't exist
    job = get_object_or_404(AddJobModel, id=job_id)

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Update the job instance with the submitted data
        job.job_title = request.POST.get('job_title')
        job.company_name = request.POST.get('company_name')
        job.location = request.POST.get('location')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.salary = request.POST.get('salary')
        
        # Save the changes to the database
        job.save()
        
        # Provide feedback to the user
        messages.success(request, 'Job updated successfully.')
        
        # Redirect to the page that lists all created jobs
        return redirect('CreatedJob')

    # If not a POST request, render the edit job template with the job instance
    return render(request, 'myAdmin/editJob.html', {'job': job})

@login_required
def delete_job(request, job_id):
    # Get the job to delete
    job = get_object_or_404(AddJobModel, id=job_id)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('CreatedJob')
    
    context = {
        'job': job
    }
    
    return render(request, 'myAdmin/deleteJob.html', context)
