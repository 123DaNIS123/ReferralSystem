from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator

from django.utils import timezone

from django.utils.translation import gettext_lazy

from .managers import CustomUserManager

from .extension import utils

class CustomUser(AbstractBaseUser):
    
    invitation_code = models.CharField(primary_key=True, default=utils.get_random_string(6), unique=True, null=False, blank=True)

    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16, blank=True, unique=True)

    invited_by = models.ForeignKey("self", null=True, blank=True, max_length=6, on_delete=models.SET_NULL)
    otp_valid_until = models.DateTimeField(default=timezone.now, null=False, blank=True)
    password = models.CharField(max_length=128, null=True)    

    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return str(self.phone_number)
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
