from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Dashboard


class DashboardListView(ListView):
    model = Dashboard
    template_name = 'dashboards/list.html'
    context_object_name = 'dashboards'

    def get_queryset(self):
        return Dashboard.objects.prefetch_related('teams').all()


class DashboardDetailView(DetailView):
    model = Dashboard
    template_name = 'dashboards/detail.html'

    def get_queryset(self):
        return Dashboard.objects.prefetch_related('teams', 'teams__users')


class DashboardCreateView(LoginRequiredMixin, CreateView):
    model = Dashboard
    fields = ['name', 'title', 'description', 'teams']
    template_name = 'dashboards/form.html'
    success_url = reverse_lazy('dashboards:list')


class DashboardUpdateView(LoginRequiredMixin, UpdateView):
    model = Dashboard
    fields = ['name', 'title', 'description', 'teams']
    template_name = 'dashboards/form.html'
    success_url = reverse_lazy('dashboards:list')


class DashboardDeleteView(LoginRequiredMixin, DeleteView):
    model = Dashboard
    template_name = 'dashboards/confirm_delete.html'
    success_url = reverse_lazy('dashboards:list')


class DashboardAccessView(LoginRequiredMixin, ListView):
    model = Dashboard
    template_name = 'dashboards/access.html'
    context_object_name = 'dashboards'

    def get_queryset(self):
        return (
            Dashboard.objects.filter(teams__users=self.request.user)
            .prefetch_related('teams')
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = self.request.user.teams.prefetch_related('dashboards').all()
        context['user_teams'] = teams
        context['all_teams'] = teams
        context['team_options'] = teams
        return context