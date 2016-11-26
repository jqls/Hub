from django.contrib import admin

from workflow.models.parameter import Parameter, ParameterText, ParameterSelection, ParameterSelectionChoice
from workflow.models.processor import *


class ProcessorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Processor, ProcessorAdmin)
admin.site.register(Parameter)
admin.site.register(ParameterText)
admin.site.register(ParameterSelection)
admin.site.register(ParameterSelectionChoice)
