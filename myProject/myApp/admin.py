from django.contrib import admin

from myApp.models import *


admin.site.register(CustomUser)
admin.site.register(ResumeModel)
admin.site.register(Education_model)
admin.site.register(Language_Model)
admin.site.register(Interest_Model)
admin.site.register(Experience_Model)
admin.site.register(Skill_model)
