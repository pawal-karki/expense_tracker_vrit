from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    key = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Email verification for {self.user.username}"
    
    def is_expired(self):
        #Check if the verification key has expired (15 minutes)
        expiry_time = self.created_at + timedelta(minutes=15)

        return timezone.now() > expiry_time
    
    def verify(self):
        """when the email as verified"""
        self.is_verified = True
        self.verified_at = timezone.now()
        self.user.is_active = True  # Activate the user account
        self.user.save()
        self.save()
