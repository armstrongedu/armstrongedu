from datetime import datetime

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.gis.geoip2 import GeoIP2
from cryptography.fernet import Fernet

from course.models import Category, Course
from payment.models import MembershipType
from authorization.models import Student

from .utils import localize, gen_cert

member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/')



def home(request):
    user = request.user
    if user.is_authenticated and user.is_member() and user.has_students():
        if request.COOKIES.get('std_id') and request.COOKIES.get('std'):
            return redirect('course:courses')
        else:
            return redirect('authorization:set-student')


    g = GeoIP2()
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
    try:
        country = g.country(client_ip).get('country_name')
    except Exception:
        localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    else:
        localized_membership_type = MembershipType.objects.filter(country=country)
        if not localized_membership_type.exists():
            localized_membership_type = MembershipType.objects.filter(country=MembershipType.INTERNATIONAL)
    context = {
        'membership_types': localized_membership_type,
        'courses': Course.objects.filter(is_featured=True),
    }
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        context['min_age'] = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        context['max_age'] = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
    return render(template_name=localize('home.html'), request=request, context=context)


@login_required
def cert(request, cert_id):
    course_id, std_id = cert_id.split('-')
    course = Course.objects.get(id=course_id)
    std = Student.objects.get(id=std_id)
    gen_cert(course, std)
    context = {
        'cert_url': f'/uploads/{cert_id}.pdf',
    }

    return render(template_name=localize('masterstudy/cert.html'), request=request, context=context)


def terms(request):
    return render(template_name=localize('masterstudy/terms.html'), request=request)


def privacy(request):
    return render(template_name=localize('masterstudy/privacy.html'), request=request)
