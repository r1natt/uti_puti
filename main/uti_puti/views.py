from icecream import ic

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import User, Course, CoursesGroup, View
from .forms import RegisterForm
from django.core.exceptions import ObjectDoesNotExist

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

def prices(request):
    return render(request, 'prices.html', {"user": request.user})

def get_nested_lists(input_list, dim):
    """
    В процессе верстки страниц курсов и курсов в профиле нам нужно распределить
    одномерный список курсов по строкам из 3-х, 4-х ячеек с этими курсами,
    данная функция получает на вход список, который нужно распределить на строки
    с элементами в количестве dim штук
    
    Примеры:
    Вход: 
        input_list = [1, 2, 3, 4, 5, 6] 
        n = 5
    Выход:
        [[1, 2, 3, 4, 5], [6, None, None, None, None]]

    Вход: 
        input_list = [1, 2, 3, 4, 5, 6] 
        n = 3
    Выход:
        [[1, 2, 3], [4, 5, 6]]

    Вход: 
        input_list = [1, 2, 3] 
        n = 3
    Выход:
        [[1, 2, 3]]

    """

    dims = []
    
    list_of_dim = [None for _ in range(dim)]
    for n, course in enumerate(input_list):
        del list_of_dim[n % dim]
        list_of_dim.insert(n % dim, course)
        if n + 1 == dim:
            dims.append(list_of_dim)
            list_of_dim = [None for _ in range(dim)]

    if any(list_of_dim):
        dims.append(list_of_dim)

    return dims

def get_courses_threes():
    data = {}

    courses_group = CoursesGroup.objects.all()

    for course_group in courses_group:
        courses_in_group = course_group.courses.all()
        data[course_group.name] = get_nested_lists(courses_in_group, 3)
    return data

@login_required
def courses(request):
    data = get_courses_threes()
    return render(
        request, 
        'courses.html', 
        {
            "user": request.user,
            "data": data,
            "course_obj": Course
        }
    )

@login_required
def video_page(request, course_id):
    if request.method == "POST":
        is_viewed_before = bool(View.objects.filter(user=request.user, course=Course.objects.get(id=course_id)).all())
        print(is_viewed_before)
        if not is_viewed_before:
        
            view = View(
                user=request.user,
                course=Course.objects.get(id=course_id)
            )
            view.save()
        return redirect('courses')

    course = Course.objects.get(id=course_id)
    return render(request, 'video_page.html', {
            "user": request.user,
            "course": course
        }
    )

def get_viewed_data(user):
    try:
        views = View.objects.filter(user=user)
    except ObjectDoesNotExist:
        views = []
    return views

@login_required
def profile(request):
    viewed_videos = get_viewed_data(request.user)
    viewed_nested_list = get_nested_lists(viewed_videos, 4)
    print(viewed_nested_list)
    return render(
        request, 
        'profile.html', 
        {
            "user": request.user, 
            "courses_dims": viewed_nested_list
        }
    )

@login_required
def rates(request):
    return render(
        request, 
        'rates.html', 
        {
            "user": request.user
        }
    )