from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

from course.models import Course, Lesson, Topic, Track


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/authorization/add-students/')

def courses(request):
    context = {
        'courses': Course.objects.all(),
        'tracks': Track.objects.all(),
    }
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        context['min_age'] = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        context['max_age'] = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
    return render(template_name=f'masterstudy/courses{_ar if settings.LANG == "ar" else ""}.html', request=request, context=context)

def course(request, course_id):
    context = {
        'course': get_object_or_404(Course, id=course_id),
        'lessons': Lesson.objects.filter(course_id=course_id).order_by('order'),
    }
    return render(template_name=f'masterstudy/course{_ar if settings.LANG == "ar" else ""}.html', request=request, context=context)


@login_required
@member_required
@students_required
def start(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    course = topic.lesson.course
    prev_lesson = Lesson.objects.filter(course_id=course, order=topic.lesson.order-1).first()
    next_lesson = Lesson.objects.filter(course_id=course, order=topic.lesson.order+1).first()
    context = {
        'course': course,
        'lessons': Lesson.objects.filter(course_id=course).order_by('order'),
        'topic': topic,
        'prev_topic': (Topic.objects.filter(lesson__course_id=course, lesson=topic.lesson, order=topic.order-1).first() or
                       (prev_lesson.topics.all().last() if prev_lesson else None)),
        'next_topic': (Topic.objects.filter(lesson__course_id=course, lesson=topic.lesson, order=topic.order+1).first() or
                       (next_lesson.topics.all().first() if next_lesson else None)),
    }
    return render(template_name=f'masterstudy/lesson{_ar if settings.LANG == "ar" else ""}.html', request=request, context=context)
