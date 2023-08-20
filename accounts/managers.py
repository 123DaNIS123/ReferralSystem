from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number is not given")
        
        
        user = self.model(phone_number=phone_number, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_staffuser(self, phone_number, password=None, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        user = self.create_user(phone_number, password, **extra_fields)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff = True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser = True")
        user = self.create_user(phone_number, password, **extra_fields)
        return user