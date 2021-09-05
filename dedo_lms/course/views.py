from django.shortcuts import render, get_object_or_404
from course.models import Course


def courses(request):
    context = {
        # 'categories': Category.objects.all(),
        'courses': Course.objects.all(),
    }
    return render(template_name='masterstudy/courses.html', request=request, context=context)

def course(request, course_id):
    context = {
        'course': get_object_or_404(Course, id=course_id)
    }
    return render(template_name='masterstudy/course.html', request=request, context=context)
