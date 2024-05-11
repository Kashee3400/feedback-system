from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

# Define a list of URL paths that should be excluded from login redirection
API_URLS = ['/api/','/vet/api/','/route/']

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if not request.user.is_authenticated:
            # Check if the request is made to an API endpoint
            for api_url in API_URLS:
                if request.path.startswith(api_url):
                    # If the request is made to an API endpoint, allow access without authentication
                    return response

            # If user is not authenticated and the request is not made to an API endpoint,
            # redirect to login page
            login_url = reverse(settings.LOGIN_URL)
            if request.path != login_url:
                return redirect('{}?next={}'.format(login_url, '/'))
        else:
            # If user is authenticated, redirect based on role or status
            if request.path == reverse(settings.LOGIN_URL):
                if request.user.is_superuser or  request.user.is_staff:
                    return redirect(reverse('dashboard'))  # Example URL for admin dashboard
                elif request.user.role.role == 'HOD':
                    return redirect(reverse('hod_feedback_list'))
                else:
                    return redirect(reverse('feedback_list'))   # Example URL for regular user dashboard

        return response
