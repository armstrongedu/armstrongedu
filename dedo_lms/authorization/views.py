from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import SignUpForm
from .utils import login_excluded


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('authorization:login')
    template_name = 'registration/signup.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_excluded('parking_page:parking_page')(view)

# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required

# @login_required
# def my_view(request):
#     ...
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'
#     ...
#
# from django.contrib.auth.decorators import user_passes_test
#
# def email_check(user):
#         return user.email.endswith('@example.com')
#
# @user_passes_test(lambda user: user.is_confirmed)
# def my_view(request):
#     ...
#
# from django.contrib.auth.mixins import UserPassesTestMixin
#
# class MyView(UserPassesTestMixin, View):
#
#     def test_func(self):
#         return self.request.user.email.endswith('@example.com')
#
# from .permissions import UserPermission


# def register(request):
#     '''
#     Registers a new user account and sends a confirmation link
#     '''
#     user_ser = UserSerializer(data=request.data)
#     if not user_ser.is_valid():
#         return Response(
#             {'details': user_ser.errors},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     username = user_ser.save()
#     user_model = get_user_model()
#     user = user_model.objects.get(username=username)
#     token = str(RefreshToken.for_user(user).access_token)
#     return Response({'token': token}, status=status.HTTP_201_CREATED)
#
# def check_email(request):
#     '''
#     Checks if the Email is used or not
#     '''
#     user_model = get_user_model()
#     return Response({'details': user_model.objects.filter(email=request.GET['email']).exists()})
#
# def check_username(request):
#     '''
#     Checks if the Username is used or not
#     '''
#     user_model = get_user_model()
#     return Response({'details': user_model.objects.filter(username=request.GET['username']).exists()})
#
# def confirm_email(request):
#     '''
#     Confirms the authed user's email using the code
#     '''
#     request.user.confirm_email(request.data['code'])
#     return Response({'details': request.user.is_confirmed})
