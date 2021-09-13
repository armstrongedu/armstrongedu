from django.shortcuts import render

from course.models import Category, Course


def home(request):
    context = {
        'courses': Course.objects.all(),
    }
    return render(template_name='home.html', request=request, context=context)
