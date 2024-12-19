from django.contrib import admin
from .models import Course, CoursesGroup, View


# Register your models here.
admin.site.register(Course)
admin.site.register(CoursesGroup)
admin.site.register(View)