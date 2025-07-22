from django.urls import path
from ..views import instructor

app_name = 'instructor'

urlpatterns = [
    path('courses/', instructor.CourseListView.as_view(), name="course_list"),
    path('course/create', instructor.CourseCreateView.as_view(), name="course_create"),
    path('course/<int:pk>/edit/',
         instructor.CourseUpdateView.as_view(), name="course_edit"),
    path('course/<int:pk>/delete/',
         instructor.CourseDeleteView.as_view(), name="course_delete")
]
