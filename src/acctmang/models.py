from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save



class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('Username must be provided')
        if not email:
            raise ValueError('Email address must be provided')
        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    email = models.EmailField('email', unique=True, blank=False, null=False)
    username = models.CharField(
        'username', blank=False, unique=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)

    objects = UserAccountManager()

    def get_username(self):
        return str(self.username)

    def __str__(self):
        return str(self.email)


class EmailOrUsernameModelBackend(object):
    """
    Class allows authentication with either a username or an email address.

    """

    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None


class Profile(models.Model):
    """
    User Profiles )( Followership
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="profile")
    slug = models.SlugField(unique=True)
    firstname = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    tstack = models.CharField(max_length=500, blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=300, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.slug)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        create = Profile.objects.create(user=kwargs['instance'], slug=kwargs['instance'].username)


post_save.connect(create_profile, sender=User)