from django.shortcuts import render, get_object_or_404
from course.models import Course, Lesson, Topic, Track


def courses(request):
    context = {
        'courses': Course.objects.all(),
        'tracks': Track.objects.all(),
    }
    return render(template_name='masterstudy/courses.html', request=request, context=context)

def course(request, course_id):
    context = {
        'course': get_object_or_404(Course, id=course_id),
        'lessons': Lesson.objects.filter(course_id=course_id).order_by('order'),
    }
    return render(template_name='masterstudy/course.html', request=request, context=context)

def start(request, topic_id): # NOTE(gaytomycode): this is tmp
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
    return render(template_name='masterstudy/lesson.html', request=request, context=context)
