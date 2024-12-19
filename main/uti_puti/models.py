from django.db import models
from django.contrib.auth.models import User


class CoursesGroup(models.Model):
    name = models.CharField(max_length=200)

class Course(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000, default="")
    pic_name = models.CharField(max_length=100)
    video_name = models.CharField(max_length=100)
    courses_group = models.ForeignKey(CoursesGroup, related_name='courses', on_delete=models.CASCADE, null=True)

class View(models.Model):
    user = models.ForeignKey(User, related_name='user_views', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='course', on_delete=models.DO_NOTHING)