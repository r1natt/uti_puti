from icecream import ic

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import User, Course, CoursesGroup
from .forms import RegisterForm

# from .course_structure import course_data

from django.http import HttpResponse


def index(request):
    return render(request, "index.html", {"user": request.user})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})

def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
        else:
            error_message = "Invalid credentials"
    return render(request, 'login.html', {'error': error_message})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    return render(request, 'profile.html', {"user": request.user})

@login_required
def courses(request):
    data = {}

    courses_group = CoursesGroup.objects.all()

    for course_group in courses_group:
        data[course_group] = course_group.courses.all()
        courses_threes = []
        three = []
        for course in course_group.courses.all():
            if len(three) == 3:
                courses_threes.append(three)
                three = []
            three.append(course)
        if len(three) == 1:
            three.append(-1)
            three.append(-1)
        if len(three) == 2:
            three.append(-1)
    ic(data)
    return render(
        request, 
        'courses.html', 
        {
            "user": request.user,
            "courses_group": courses_group
        }
    )

@login_required
def video_page(request, course_id):
    
    return render(request, 'video_page.html', {
            "user": request.user,
            
        }
    )
