from django.contrib import admin

from form.models import *

class ApplyModelFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'cv')

admin.site.register(JobApplication, ApplyModelFormAdmin)
