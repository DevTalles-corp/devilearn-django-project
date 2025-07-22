
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from ..models import Course


class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_instructor


class CourseListView(InstructorRequiredMixin, ListView):
    model = Course
    template_name = 'instructor/course_list.html'
    context_object_name = "courses"
    paginate_by = 8

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)
