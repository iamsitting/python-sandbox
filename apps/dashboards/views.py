import csv
from pathlib import Path

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
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


class DashboardCustomerDataView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboards/customer_data.html'

    def dispatch(self, request, *args, **kwargs):
        self.dashboard = Dashboard.objects.prefetch_related('teams').filter(pk=kwargs['pk']).first()
        if self.dashboard is None:
            raise Http404('Dashboard not found')
        if self.dashboard.pk != 1:
            raise Http404('Customer data is only available for dashboard 1')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        csv_path = Path(settings.BASE_DIR) / 'data' / 'customers.csv'
        rows = []
        status_counts = {}

        if csv_path.exists():
            with csv_path.open(newline='', encoding='utf-8') as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    rows.append(row)
                    status = row.get('status', 'Unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1

        context['dashboard'] = self.dashboard
        context['customer_rows'] = rows
        context['status_labels'] = list(status_counts.keys())
        context['status_values'] = list(status_counts.values())
        context['customer_count'] = len(rows)
        context['csv_missing'] = not csv_path.exists()
        return context