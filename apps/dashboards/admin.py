from django.contrib import admin

from .models import Dashboard, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_count', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['users']

    def user_count(self, obj):
        return obj.users.count()

    user_count.short_description = 'Users'


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'team_count', 'created_at']
    search_fields = ['name', 'title', 'description']
    filter_horizontal = ['teams']

    def team_count(self, obj):
        return obj.teams.count()

    team_count.short_description = 'Teams'