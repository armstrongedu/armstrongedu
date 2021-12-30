from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views
from . import forms


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True, authentication_form=forms.LoginForm),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(extra_context = {'form': forms.LoginForm}),
        name='logout'
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('authorization:password_reset_done'),
            form_class=forms.PasswordResetForm,
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            extra_context = {'form': forms.LoginForm}
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('authorization:password_reset_complete'),
            form_class=forms.SetPasswordForm,
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            extra_context = {'form': forms.LoginForm}
        ),
        name='password_reset_complete'
    ),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('add-students/', views.add_students, name='add-students'),
    path('set-student/', views.set_student, name='set-student'),
    path('switch-students/<std_id>', views.switch_students, name='change-std'),
    path('confirm-email-start/', views.confirm_email_start,
         name='confirm-email-start'),
    path('confirm-email/', views.confirm_email,
         name='confirm-email'),
    path('confirm-email/<key>', views.confirm_email,
         name='confirm-email-key'),
    path('email-confirmed/', views.email_confirmed,
         name='email-confirmed'),
    path('newsletter/', views.newsletter,
         name='newsletter'),
    path('profile/', views.profile,
         name='profile'),
]
