from django.contrib.sessions.models import Session


class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            stored_session_key = request.user.login_sessions.session_key

            if stored_session_key and stored_session_key != request.session.session_key:
                try:
                    Session.objects.get(session_key=stored_session_key).delete()
                except Session.DoesNotExist:
                    pass

            request.user.login_sessions.session_key = request.session.session_key
            request.user.login_sessions.save()

        response = self.get_response(request)

        return response
