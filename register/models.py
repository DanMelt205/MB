from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime


class UserManager(BaseUserManager):

    def create_user(self, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        print(kwargs.get('last_name'), kwargs.get(
            'first_name'), kwargs.get('email'), kwargs.get('date_of_birth'),
            kwargs.get('security_question'), kwargs.get('security_answer'),
            kwargs.get('user_type'), kwargs.get('password'))

        if not kwargs.get('email'):
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(kwargs.get('email')),
        )
        user.first_name = kwargs.get('first_name')
        user.last_name = kwargs.get('last_name')
        user.username = self.create_username(
            kwargs.get('first_name'), kwargs.get('last_name'))
        user.date_of_birth = kwargs.get('date_of_birth')
        user.security_question = kwargs.get('security_question')
        user.security_answer = kwargs.get('security_answer')
        user.user_type = kwargs.get('user_type')
        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_staffuser(self, **kwargs):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=kwargs.get('email'),
            password=kwargs.get('password'),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            date_of_birth=kwargs.get('date_of_birth'),
            security_question=kwargs.get('security_question'),
            security_answer=kwargs.get('security_answer'),
            user_type=kwargs.get('user_type'),
            username=self.create_username(
                kwargs.get('first_name'), kwargs.get('last_name'))
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=kwargs.get('email'),
            password=kwargs.get('password'),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            date_of_birth=kwargs.get('date_of_birth'),
            security_question=kwargs.get('security_question'),
            security_answer=kwargs.get('security_answer'),
            user_type=kwargs.get('user_type'),
            username=self.create_username(
                kwargs.get('first_name'), kwargs.get('last_name'))
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def create_username(self, first_name, last_name):
        dateM = datetime.now().strftime("%m")
        dateY = datetime.now().strftime("%y")
        return str(first_name[0] + last_name + dateM + dateY).lower()


class User(AbstractBaseUser):

    user_types = (
        (1, "Accountant"),
        (2, "Manager"),
        (3, "Admin"),
    )

    security_questions = (
        (1, "Whats is your mother maiden name?"),
        (2, "What is your favorite color?"),
        (3, "What is your biggest fear?"),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    password_expiration = models.IntegerField(default=0)
    user_type = models.IntegerField(choices=user_types, default=1)
    date_of_birth = models.DateField(null=True)
    security_question = models.IntegerField(
        choices=security_questions, null=True)
    security_answer = models.CharField(max_length=100, null=True)
    deactive_time_start = models.DateField(null=True, blank=True)
    deactive_time_end = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=150, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'date_of_birth', 'security_question',
                       'security_answer', 'user_type']

    objects = UserManager()

    class Meta:
        ordering = ['-date_joined']

    def get_absolute_url(self):
        return reverse('email', kwargs={'pk': self.pk})

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
