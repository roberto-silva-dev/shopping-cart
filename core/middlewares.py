from django.utils.deprecation import MiddlewareMixin


class EnsureSessionKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.session_key:
            request.session.create()
