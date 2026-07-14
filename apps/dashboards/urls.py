from django.urls import path

from .views import DashboardAccessView, DashboardCreateView, DashboardCustomerDataView, DashboardDeleteView, DashboardDetailView, DashboardListView, DashboardUpdateView

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardListView.as_view(), name='list'),
    path('access/', DashboardAccessView.as_view(), name='access'),
    path('create/', DashboardCreateView.as_view(), name='create'),
    path('<int:pk>/', DashboardDetailView.as_view(), name='detail'),
    path('<int:pk>/customers/', DashboardCustomerDataView.as_view(), name='customer-data'),
    path('<int:pk>/edit/', DashboardUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', DashboardDeleteView.as_view(), name='delete'),
]