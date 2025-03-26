import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel


class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.ROLE_SAAS_ADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the Liquor Shop Management System.
    Uses email as the unique identifier instead of username.
    """
    # User roles
    ROLE_SAAS_ADMIN = 'saas_admin'
    ROLE_TENANT_ADMIN = 'tenant_admin'
    ROLE_MANAGER = 'manager'
    ROLE_ASSISTANT_MANAGER = 'assistant_manager'
    ROLE_EXECUTIVE = 'executive'
    
    ROLE_CHOICES = [
        (ROLE_SAAS_ADMIN, _('SaaS Admin')),
        (ROLE_TENANT_ADMIN, _('Tenant Admin')),
        (ROLE_MANAGER, _('Manager')),
        (ROLE_ASSISTANT_MANAGER, _('Assistant Manager')),
        (ROLE_EXECUTIVE, _('Executive')),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=150)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    
    # Tenant information
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    # Role information
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default=ROLE_EXECUTIVE)
    
    # Status fields
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active.'),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into the admin site.'),
    )
    
    # Timestamps
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)
    
    # Additional fields
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['email']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email
    
    def is_tenant_admin(self):
        return self.role == self.ROLE_TENANT_ADMIN
    
    def is_manager(self):
        return self.role == self.ROLE_MANAGER
    
    def is_assistant_manager(self):
        return self.role == self.ROLE_ASSISTANT_MANAGER
    
    def is_executive(self):
        return self.role == self.ROLE_EXECUTIVE
    
    def is_saas_admin(self):
        return self.role == self.ROLE_SAAS_ADMIN
    
    def lock_account(self, duration_minutes=30):
        """
        Lock the user account for the specified duration.
        """
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])
    
    def unlock_account(self):
        """
        Unlock the user account.
        """
        self.account_locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
    
    def is_account_locked(self):
        """
        Check if the user account is locked.
        """
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        elif self.account_locked_until:
            # If lock has expired, unlock the account
            self.unlock_account()
        return False
    
    def increment_failed_login(self):
        """
        Increment the failed login attempts counter and lock the account if necessary.
        """
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        
        # Lock account after 5 failed attempts
        if self.failed_login_attempts >= 5:
            self.lock_account()
            
        self.save(update_fields=['failed_login_attempts', 'last_failed_login', 'account_locked_until'])
    
    def reset_failed_login(self):
        """
        Reset the failed login attempts counter.
        """
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])


class UserShopAssignment(BaseModel):
    """
    Model to track which shops a user is assigned to.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_assignments')
    shop_id = models.UUIDField()
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'shop_id')
        verbose_name = _('user shop assignment')
        verbose_name_plural = _('user shop assignments')
    
    def __str__(self):
        return f"{self.user.email} - {self.shop_id}"


class UserPermission(BaseModel):
    """
    Model to store custom permissions for users beyond their role-based permissions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_permissions')
    permission_key = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('user', 'permission_key')
        verbose_name = _('user permission')
        verbose_name_plural = _('user permissions')
    
    def __str__(self):
        return f"{self.user.email} - {self.permission_key}"