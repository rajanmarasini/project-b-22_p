
# Create your models here.

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib import admin
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth.models import User #add this
from django.db.models import Avg, Count
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from isbn_field import ISBNField

class UserManager(BaseUserManager):

  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        username=username,
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self,username, email, password, **extra_fields):
    return self._create_user(username, email, password, False, False, **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    user=self._create_user(username, email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user

class Textbooks(models.Model):
    name = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=255, null=False)
    condition = models.CharField(max_length=255, null=False)
    creator = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default = 0, validators=[MinValueValidator(Decimal(0.00))]) 
    course = models.CharField(max_length=255, null=False, default="")
    instructor = models.CharField(max_length=255, null=False, default="")
    isbn = ISBNField()
    likes = models.IntegerField(default=0)
    def negCheck(price):
        if (price < 0):
            raise ValidationError('Cannot enter a negative value.')
    def __str__(self):
        return "{} - {} - {}".format(self.author, self.condition, self.price, self.creator,selfUser = models.ForeignKey(User, on_delete=models.CASCADE).name)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def averageReview(self):
        reviews = Rating.objects.filter(User=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = Rating.objects.filter(User=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count   

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [ 'email']

    objects = UserManager()
    favorites = models.ManyToManyField(Textbooks, related_name='favorited_by')
    posts = models.ManyToManyField(Textbooks, related_name='posted_by')

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)

    LOCATION_OPTIONS = (
    ("On Grounds", "On Grounds"),
    ("Off Grounds", "Off Grounds"),
    )
    YEAR_OPTIONS = (
    ("1", "1st year"),
    ("2", "2nd year"),
    ("3", "3rd year"),
    ("4", "4th year"),
    )
    year = models.CharField(max_length=15, choices=YEAR_OPTIONS, default=YEAR_OPTIONS[0][1])
    location = models.CharField(max_length=15, choices=LOCATION_OPTIONS, default=LOCATION_OPTIONS[0][1])
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    major = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user)

# Add Location (as multiple choice and make a default rating
    def __str__(self):
        return self.year

class ProfileForms(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'major', 'year', 'location', 'email']

class Rating(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    status = models.BooleanField(default=True)


