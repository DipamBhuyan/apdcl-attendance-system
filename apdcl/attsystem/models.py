from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group,Permission
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Password should be hashed, so max_length=128 is recommended
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    office = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100,blank=True, null=True)
    boss_name = models.CharField(max_length=100, blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender=models.CharField(max_length=10, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    request_date = models.DateField(auto_now=True)
    request_response_date = models.DateField(blank=True, null=True)
    is_boss = models.BooleanField(default=False)
    is_response = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname', 'phone', 'office', 'designation',]

    def __str__(self):
        return self.email
    
class attendance(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    status = models.CharField(max_length=10, default='Pending')
    archive_status = models.CharField(max_length=10, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_respond = models.BooleanField(default=False)
    approved_date = models.DateField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class holiday_list(models.Model):
    date = models.DateField()
    occasion = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
