from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import Q
# Create your models here.




class AboutUs(models.Model):
       maintitle = models.CharField(max_length=200)
       description = RichTextField()
       title1 = models.CharField(max_length=200)
       point1 = models.CharField(max_length=200)
       title2 = models.CharField(max_length=200)
       point2 = models.CharField(max_length=200)
       title3= models.CharField(max_length=200)
       point3 = models.CharField(max_length=200)


       def __str__(self):
          return self.maintitle 

class Home(models.Model):
       maintitle = models.CharField(max_length=200)
       maintitle2 = models.CharField(max_length=200)
       card1 = models.CharField(max_length=200)
       description1 = models.CharField(max_length=200)
       card2 = models.CharField(max_length=200)
       description2 = models.CharField(max_length=200)
       card3= models.CharField(max_length=200)
       description3 = models.CharField(max_length=200)
       card4= models.CharField(max_length=200)
       description4 = models.CharField(max_length=200)
       



       def __str__(self):
          return self.maintitle 
#################################################################
class College_List(models.Model):
    college_Name = models.CharField(max_length=80)
    college_Country = models.CharField(max_length=20)
    college_City = models.CharField(max_length=50)
    college_Subcity = models.CharField(max_length=80)
    college_Email = models.EmailField(unique=True)
    college_Description = models.CharField(max_length=500)
    college_phone = models.CharField(max_length=20)

class College_Requirements(models.Model):
    Rcollege = models.OneToOneField(College_List, on_delete=models.CASCADE)
    Matric_Requirement = models.CharField(max_length=10)
    GPA_Requirement = models.CharField(max_length=10)
    ExtraCurricular_Requirement = models.CharField(max_length=300)
    
class College_Fields(models.Model):
    NATURAL_SCIENCE = 'NS'
    SOCIAL_SCIENCE = 'SS'
    FIELD_BRANCH_CHOICES = [
        (NATURAL_SCIENCE, 'Natural Science'),
        (SOCIAL_SCIENCE, 'Social Science'),
    ]

    ENGINEERING = 'Engineering'
    HEALTH = 'Health'
    IT = 'IT'
    BUSINESS = 'Business'
    HISTORY = 'History'
    FIELD_CATEGORY_CHOICES = [
        (ENGINEERING, 'Engineering'),
        (HEALTH, 'Health'),
        (IT, 'IT'),
        (BUSINESS, 'Business'),
        (HISTORY, 'History'),
    ]

    college = models.ForeignKey(College_List, on_delete=models.CASCADE)
    Field_Name = models.CharField(max_length=100)
    Field_Branch = models.CharField(max_length=2, choices=FIELD_BRANCH_CHOICES)
    Field_Category = models.CharField(max_length=20, choices=FIELD_CATEGORY_CHOICES)

    def __str__(self):
        return self.Field_Name
#####################################################
class CustomUser(AbstractUser):
   
    HIGHER_EDUCATION = 'highereducation'
    STUDENT = 'student'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        ('', 'Choose your role'),
        (HIGHER_EDUCATION, 'highereducation'),
        (STUDENT , 'student '),
        (ADMIN, 'Admin'),
    ]

   
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    email = models.EmailField(unique=True)

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    def __str__(self):
        return self.username
    
