from django.shortcuts import render

from course.models import Category, Course
from payment.models import MembershipType


def home(request):
    context = {
        'membership_types': MembershipType.objects.all(),
        'courses': Course.objects.all(),
    }
    return render(template_name='home.html', request=request, context=context)
