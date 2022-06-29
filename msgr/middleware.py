
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve


class LoginRequiredMiddleware:
    """Limit access to an entire app to authenticated users."""

    RESTRICTED_APP = "msgr"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, "user"):
            raise ImproperlyConfigured("Requires the django's authentication"
                                       " middleware to be installed.")

        if not request.user.is_authenticated:
            if resolve(request.path).app_name == self.RESTRICTED_APP:
                return redirect_to_login(request.get_full_path())

        return self.get_response(request)
