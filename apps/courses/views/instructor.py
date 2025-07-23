
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..models import Course, Module, Content
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404


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


class CourseUpdateView(InstructorRequiredMixin, UpdateView):
    model = Course
    fields = ['title', 'slug', 'overview',
              'image', 'level', 'duration', 'categories']
    template_name = 'instructor/course_form.html'
    success_url = reverse_lazy('instructor:course_list')

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)


class CourseDeleteView(InstructorRequiredMixin, DeleteView):
    model = Course
    template_name = 'instructor/course_confirm_delete.html'
    success_url = reverse_lazy('instructor:course_list')

    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

# Module Views


class ModuleListView(InstructorRequiredMixin, ListView):
    model = Module
    template_name = 'instructor/module_list.html'
    context_object_name = "modules"

    def get_queryset(self):
        self.course = get_object_or_404(
            Course, id=self.kwargs['course_id'], owner=self.request.user)
        return self.course.modules.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context


class ModuleCreateView(InstructorRequiredMixin, CreateView):
    model = Module
    fields = ['title', 'description']
    template_name = 'instructor/module_form.html'

    def form_valid(self, form):
        course = get_object_or_404(
            Course, id=self.kwargs['course_id'], owner=self.request.user)
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('instructor:module_list', args=[self.object.course.id])


class ModuleUpdateView(InstructorRequiredMixin, UpdateView):
    model = Module
    fields = ['title', 'description']
    template_name = 'instructor/module_form.html'

    def get_queryset(self):
        return Module.objects.filter(course__owner=self.request.user)

    def get_success_url(self):
        return reverse('instructor:module_list', args=[self.object.course.id])


class ModuleDeleteView(InstructorRequiredMixin, DeleteView):
    model = Module
    template_name = 'instructor/module_confirm_delete.html'

    def get_queryset(self):
        return Module.objects.filter(course__owner=self.request.user)

    def get_success_url(self):
        return reverse('instructor:module_list', args=[self.object.course.id])

# Content


class ContentListView(InstructorRequiredMixin, ListView):
    model = Content
    template_name = 'instructor/content_list.html'
    context_object_name = "contents"

    def get_queryset(self):
        self.module = get_object_or_404(
            Module, id=self.kwargs['module_id'], course__owner=self.request.user)
        return self.module.contents.all().select_related('content_type').order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = self.module
        return context
