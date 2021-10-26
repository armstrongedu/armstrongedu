from django.shortcuts import redirect

from . models import Student


def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if hasattr(request, 'user') and request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def create_trial_student(user):
    Student.objects.create(user=user, name='Trial Student', birth_year='0000')
