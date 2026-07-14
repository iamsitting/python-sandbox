from django.urls import path

from .views import DashboardCreateView, DashboardDeleteView, DashboardDetailView, DashboardListView, DashboardUpdateView

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardListView.as_view(), name='list'),
    path('create/', DashboardCreateView.as_view(), name='create'),
    path('<int:pk>/', DashboardDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', DashboardUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DashboardDeleteView.as_view(), name='delete'),
]