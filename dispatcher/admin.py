# coding=utf-8
from django.contrib import admin

from dispatcher.models import *

admin.site.register(ProcessorCategory)
admin.site.register(Input)
admin.site.register(Output)
admin.site.register(DataType)


class ProcessorAdmin(admin.ModelAdmin):
    class InputInline(admin.TabularInline):
        model = Input

    class OutputInline(admin.TabularInline):
        model = Output

    class ParameterInline(admin.TabularInline):
        model = Parameter

    inlines = [InputInline, OutputInline, ParameterInline, ]


class ParameterAdmin(admin.ModelAdmin):
    fieldsets = (
        (u'参数', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('content_type', 'object_id',)
        }),
    )
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']]
    }


admin.site.register(Processor, ProcessorAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(TextParameter)
admin.site.register(SelectionParameter)
