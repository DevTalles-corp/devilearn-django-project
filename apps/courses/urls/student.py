from django.urls import path
from ..views import student

app_name = 'student'

urlpatterns = [
    path("courses/", student.course_list, name="course_list"),  # /courses
    path("detail/<str:slug>", student.course_detail, name="course_detail"),
    path("<str:slug>/lessons/", student.course_lessons, name="course_lessons")
]
