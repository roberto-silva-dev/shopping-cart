from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'user_type': user.user_type})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
