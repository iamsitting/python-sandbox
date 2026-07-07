from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User



def home(request):
	return render(request, 'core/home.html')


def health(request):
	return JsonResponse({'status': 'ok'})

def users(request):
	user_objects = User.objects
	user_objects = user_objects.filter(is_active=True)
	user_objects = user_objects.order_by('username')
	user_objects = user_objects.filter(created_at__gte='2023-01-01')
	return render(request, 'core/models.html', {'users': user_objects.all()})
