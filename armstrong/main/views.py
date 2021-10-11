from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

from course.models import Category, Course
from payment.models import MembershipType

from .utils import localize

member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/')



def home(request):
    context = {
        'membership_types': MembershipType.objects.all(),
        'courses': Course.objects.all(),
    }
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        context['min_age'] = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        context['max_age'] = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
    return render(template_name=localize('home.html'), request=request, context=context)


@login_required
@member_required
@students_required
def cert(request, cert_id):
    # TODO(gaytomycode): if the current student finished the course sent then eb3t cert
    std = Student.objects.get(user=request.user, name=std_name)
    resp = redirect('main:home')
    resp.set_cookie('std_id', std.id)
    resp.set_cookie('std', std.name)
    return resp
