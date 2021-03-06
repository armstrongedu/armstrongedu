from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import SignUpForm
from .utils import login_excluded
from .models import Student, Newsletter


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
not_students_required = user_passes_test(lambda user: not user.has_students(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/')
email_not_confirmed = user_passes_test(lambda user: not user.is_confirmed, login_url='/')

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('authorization:login')
    template_name = 'registration/signup.html'

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_excluded('main:home')(view)


@login_required
@member_required
@not_students_required
def add_students(request):
    resp = redirect('main:home')
    if request.method == 'GET':
        # request.user.students.all().delete()
        std_count = request.user.membership.number_of_students - request.user.students.count()
        cur_year = datetime.now().year
        context = {
            'range': range(cur_year, cur_year-20, -1),
            'std_range': range(0, std_count),
            'stds': request.user.students.all(),
        }
        return render(template_name=f'masterstudy/add-students{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)
    if request.method == 'POST':
        data = request.POST
        std_count = request.user.membership.number_of_students - request.user.students.count()
        for std in request.user.students.all():
            if data.get(f'name_edit_{std.id}'):
                std.image = request.FILES.get(f'image_edit_{std.id}')
                std.name = data[f'name_edit_{std.id}']
                std.birth_year = data[f'year_edit_{std.id}']
                std.save()
        for i in range(0, std_count):
            std = Student.objects.create(user=request.user, image=request.FILES.get(f'image_{i}'), name=data[f'name_{i}'], birth_year=data[f'year_{i}'])

        resp.set_cookie('std_id', std.id)
        resp.set_cookie('std', std.name)
    return resp

@login_required
@member_required
@students_required
def set_student(request):
    if request.method == 'GET':
        context = {
            'stds': Student.objects.filter(user=request.user),
        }
        return render(template_name=f'masterstudy/select-student.html', request=request, context=context)
    if request.method == 'POST':
        std_id = request.POST.get('std_id')
        std = Student.objects.get(id=std_id)
        resp = redirect('course:courses')
        resp.set_cookie('std_id', std.id)
        resp.set_cookie('std', std.name)
        return resp

@login_required
@member_required
@students_required
def switch_students(request, std_id):
    std = Student.objects.get(id=std_id)
    resp = redirect('main:home')
    resp.set_cookie('std_id', std.id)
    resp.set_cookie('std', std.name)
    return resp


@login_required
@email_not_confirmed
def confirm_email_start(request):
    context = {}
    return render(template_name='confirmation/confirm-email-start.html', request=request,
                  context=context)


@login_required
@email_not_confirmed
def confirm_email(request, key=None):
    user = request.user
    conf_key = request.POST.get('confirmation_key', key)
    user.confirm_email(conf_key)
    if user.is_confirmed:
        return redirect('authorization:email-confirmed')
    else:
        context = {
            'errors': ['Wrong Key'],
        }
        return render(template_name='confirmation/confirm-email-start.html', request=request,
                      context=context)


@login_required
def email_confirmed(request):
    context = {}
    return render(template_name='confirmation/email_confirmed.html', request=request,
                  context=context)

def newsletter(request):
    Newsletter.objects.create(email=request.POST['email'])
    return redirect('main:home')

@login_required
def profile(request):
    context = {}
    return render(template_name='masterstudy/profile.html', request=request,
                  context=context)

