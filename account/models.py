# account/models.py

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin

class UserManager(BaseUserManager):
    # FIXED: Reordered parameters to place optional 'city' after required 'password'
    def create_user(self, email, name, password, city=None, **extra_fields):
        if not email:
            raise ValueError("user must have a valid email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            city=city,
            **extra_fields # FIXED: Correctly unpacked the extra_fields dictionary
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # FIXED: Matched the reordered parameters
    def create_superuser(self, email, name, password, city=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields['is_customer'] = False   # Force overwrite
        extra_fields['is_seller'] = True   

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        # FIXED: Call create_user with the correct parameter order
        return self.create_user(email, name, password, city, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    
    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return super().has_perm(perm,obj)
    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return super().has_module_perms(app_label)
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name