from django.contrib import admin
from .models import EmailVerification


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'key', 'is_verified', 'created_at', 'verified_at']
    list_filter = ['is_verified', 'created_at', 'verified_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['key', 'created_at', 'verified_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
