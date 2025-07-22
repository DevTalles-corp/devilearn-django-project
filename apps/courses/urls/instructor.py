from django.urls import path
from ..views import instructor

app_name = 'instructor'

urlpatterns = [
    path('courses/', instructor.CourseListView.as_view(), name='course_list'),
    path('course/create', instructor.CourseCreateView.as_view(), name="course_create")
]
