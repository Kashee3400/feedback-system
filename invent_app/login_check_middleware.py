from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

API_URLS = ['/api/', '/vet/api/','/vcg/api/', '/route/']

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(api_url) for api_url in API_URLS):
            return self.get_response(request)
        if not request.user.is_authenticated:
            login_url = reverse(settings.LOGIN_URL)
            if request.path != login_url:
                return redirect(f'{login_url}?next={request.path}')
        if request.user.is_authenticated:
            if request.path == reverse(settings.LOGIN_URL):
                if request.user.is_superuser or request.user.is_staff:
                    return redirect(reverse('dashboard'))
                elif hasattr(request.user, 'role') and request.user.role.role == 'HOD':
                    return redirect(reverse('hod_feedback_list'))
                else:
                    return redirect(reverse('feedback_list')) 

        return self.get_response(request)