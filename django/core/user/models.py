from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from videodb.models.videoitem import Videoitem
from videodb.models.videoitems_list import VideoitemsList


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with an email, phone number,
        username and password.
        """
        if username is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have an username.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True, default="", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created = models.CharField(max_length=255, default="", blank=True)
    updated = models.CharField(max_length=255, default="", blank=True)

    videoitems = models.ManyToManyField(to=Videoitem)
    videoitems_lists = models.ManyToManyField(to=VideoitemsList)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"

    # def get_videoitems_lists(self) -> QuerySet:
    #     return self.videoitems_lists

    def say_hello(self) -> str:
        return "hello from " + self.username

    def create_videoitems_list(self) -> None:
        print("new list, self", self)

    def delete_videoitems_list(self) -> None:
        print("delete list, self", self)
