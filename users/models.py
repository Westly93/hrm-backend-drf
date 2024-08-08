from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .managers import UserAccountManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_resized import ResizedImageField


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name= models.CharField(max_length= 255)
    last_name= models.CharField(max_length= 255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default= False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_staff

class Profile(models.Model):
    bio= models.TextField(null=True, blank=True)
    user= models.OneToOneField(UserAccount, on_delete= models.CASCADE, related_name= "profile")
    address= models.CharField(max_length= 1000, null=True, blank=True)
    thumbnail= ResizedImageField(size= [200, 200], quality= 100, upload_to= "full_auth", 
        default= 'default.jpg')

    class Meta:
        verbose_name= "Profile"
        verbose_name_plural= "Profiles"

    def __str__(self):
        return f"{self.user.email}'s Profile"

@receiver(post_save, sender= UserAccount)
def create_profile(sender, created, instance, *args, **kwargs):
    if created:
        Profile.objects.create(user= instance)

@receiver(post_save, sender= UserAccount)
def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()