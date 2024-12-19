from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("reg/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("prices/", views.prices, name="prices"),
    path("courses/", views.courses, name="courses"),
    path("rates/", views.rates, name="rates"),
    path("courses/<int:course_id>", views.video_page, name="course_page")
]
