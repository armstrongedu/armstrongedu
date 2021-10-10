from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import SignUpForm
from .utils import login_excluded
from .models import Student


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
not_students_required = user_passes_test(lambda user: not user.has_students(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/')

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
        request.user.students.all().delete()
        std_count = request.user.membership.membership_type.number_of_students
        cur_year = datetime.now().year
        context = {
            'range': range(cur_year, cur_year-20, -1),
            'std_range': range(0, std_count),
        }
        return render(template_name=f'masterstudy/add-students{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)
    if request.method == 'POST':
        data = request.POST
        std_count = request.user.membership.membership_type.number_of_students
        for i in range(0, std_count):
            std = Student.objects.create(user=request.user, name=data[f'name_{i}'], birth_year=data[f'year_{i}'])
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
@member_required
@students_required
def gen_cert(request, std_name):
    std = Student.objects.get(user=request.user, name=std_name)
    resp = redirect('main:home')
    resp.set_cookie('std_id', std.id)
    resp.set_cookie('std', std.name)
    return resp
