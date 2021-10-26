from datetime import datetime

from django.shortcuts import render
from django.conf import settings

from course.models import Category, Course
from payment.models import MembershipType


def home(request):
    context = {
        'membership_types': MembershipType.objects.all(),
        'courses': Course.objects.all(),
    }
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        context['min_age'] = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        context['max_age'] = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
    return render(template_name=f'home{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)
