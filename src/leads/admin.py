from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ['name', 'phone', 'source', 'created', 'is_read']
    list_filter = ['source', 'is_read', 'created']
    list_editable = ['is_read']
    readonly_fields = ['name', 'phone', 'message', 'source', 'created']
    ordering = ['-created']
