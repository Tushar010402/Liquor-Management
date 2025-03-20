from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel

User = get_user_model()


class RefreshToken(BaseModel):
    """
    Model to store refresh tokens for blacklisting.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.TextField(unique=True)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Refresh Token'
        verbose_name_plural = 'Refresh Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.created_at}"


class PasswordResetToken(BaseModel):
    """
    Model to store password reset tokens.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.created_at}"


class LoginAttempt(BaseModel):
    """
    Model to track login attempts for security monitoring.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts', null=True, blank=True)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    successful = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Login Attempt'
        verbose_name_plural = 'Login Attempts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.created_at} - {'Success' if self.successful else 'Failure'}"