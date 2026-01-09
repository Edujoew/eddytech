from django.contrib import admin
from .models import Project, Message, ProjectImage, MpesaTransaction

# This allows you to add multiple gallery images on the same page as the Project
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3  # Number of empty image slots to show by default

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date_sent')
    readonly_fields = ('date_sent',)

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'status', 'created_at')
    readonly_fields = ('created_at', 'checkout_request_id')

