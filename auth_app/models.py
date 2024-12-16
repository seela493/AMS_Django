from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
# Django Django987&

Gender = [
    ('M', 'Male'),
    ('F', 'Female')
]
# Create your models here.
# what is model?
# model is the class that defines the structure of your database
# it is a blueprint for your database table and it serves as the single source of truth for your data,
# it is the interface between your application and your database

class Teacher(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=25)
    primary_number = models.CharField(max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)], unique=True, null = False, blank = False)
    secondary_number = models.CharField(
    max_length=10, 
    validators=[MinLengthValidator(10), MaxLengthValidator(10)], 
    unique=True, 
    null=True, 
    blank=True
)
    dob = models.DateField(null= True, blank= True)
    sex = models.CharField(max_length=1, choices=Gender)

    def __str__(self):
        return self.user.username
    
    # why we use class meta?

    class Meta:
        db_table = 'teacher'
        ordering = ['user']
        verbose_name = 'Teacher'
        constraints = [
            models.UniqueConstraint(fields=['primary_number', 'secondary_number'], name='unique_phone_number'),
        ]

    