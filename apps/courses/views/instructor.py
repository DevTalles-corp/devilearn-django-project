
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from ..models import Course
from django.urls import reverse, reverse_lazy


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


class CourseCreateView(InstructorRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'slug', 'overview',
              'image', 'level', 'duration', 'categories']
    template_name = 'instructor/course_form.html'
    success_url = reverse_lazy('instructor:course_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
