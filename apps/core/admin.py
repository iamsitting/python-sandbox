from django.contrib import admin

# Register your models here.

# Register the Team model in the admin site
from .models import Team
admin.site.register(Team)