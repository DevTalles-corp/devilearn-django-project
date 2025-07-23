from django.urls import path
from ..views import instructor

app_name = 'instructor'

urlpatterns = [
    path('courses/', instructor.CourseListView.as_view(), name="course_list"),
    path('course/create', instructor.CourseCreateView.as_view(), name="course_create"),
    path('course/<int:pk>/edit/',
         instructor.CourseUpdateView.as_view(), name="course_edit"),
    path('course/<int:pk>/delete/',
         instructor.CourseDeleteView.as_view(), name="course_delete"),
    # Modules URLs
    path('course/<int:course_id>/modules/',
         instructor.ModuleListView.as_view(), name='module_list'),
    path('course/<int:course_id>/modules/add',
         instructor.ModuleCreateView.as_view(), name='module_add'),
    path('modules/<int:pk>/edit/',
         instructor.ModuleUpdateView.as_view(), name='module_edit'),
    path('module/<int:pk>/delete/',
         instructor.ModuleDeleteView.as_view(), name='module_delete')
]
