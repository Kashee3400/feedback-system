from django.utils.translation import activate
from django.conf import settings
from dotenv import load_dotenv,set_key


class CustomLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user's preferred language from session, cookies, or any other source
        user_language = request.session.get('django_language') or request.COOKIES.get('django_language')
        
        # Activate the user's preferred language
        if user_language:
            activate(user_language)
            print('Activating the language')
        # Continue processing the request
        response = self.get_response(request)
        
        return response
