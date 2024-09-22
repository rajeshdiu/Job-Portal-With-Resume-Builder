from django.contrib import admin

from myApp.models import *


admin.site.register(CustomUser)
admin.site.register(BasicInfoModel)
admin.site.register(LanguageModel)
admin.site.register(IntermediateLanguageModel)
admin.site.register(IntermediateSkillModel)
admin.site.register(SkillModel)
admin.site.register(EducationModel)
admin.site.register(InstituteNameModel)
admin.site.register(DegreeModel)
admin.site.register(FieldOfStudyModel)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company_name', 'start_date', 'end_date')
    search_fields = ('job_title', 'company_name')
    

admin.site.register(ExperienceModel,ExperienceAdmin)


from django.contrib import admin
from .models import AddJobModel

class AddJobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'posted_on', 'updated_on', 'user')
    search_fields = ('job_title', 'company_name', 'location', 'user__username')
    list_filter = ('posted_on', 'updated_on', 'location', 'company_name')
    ordering = ('-posted_on',)

    # Fields to show when adding or editing a job
    fieldsets = (
        (None, {
            'fields': ('user', 'job_title', 'company_name', 'location', 'description')
        }),
        ('Dates', {
            'fields': ('posted_on', 'updated_on')
        }),
    )
    readonly_fields = ('posted_on', 'updated_on')

    

admin.site.register(AddJobModel,AddJobAdmin)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'applied_on')   # Customize fields displayed in the list view
    search_fields = ('user__username', 'job__title')  # Enable search by user and job title
    list_filter = ('job', 'user')                  # Enable filtering by job and user

admin.site.register(JobApplication, JobApplicationAdmin)



