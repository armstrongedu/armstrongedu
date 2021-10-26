from datetime import datetime, timedelta, date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils import timezone
from cryptography.fernet import Fernet

from .models import Course, Lesson, Topic, Track, Progress, MCQQuiz, TFQuiz, MCQQuizSolution, TFQuizSolution
from help_sessions.models import Period, HelpSession
from authorization.models import Student


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/authorization/add-students/')
free_trial_required = user_passes_test(lambda user: user.is_free_trial(), login_url='/payment/subscribe/')

def courses(request):
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    courses = Course.objects.filter(is_free_trial=False)
    if min_age and max_age:
        courses = courses.filter(start_age__lte=min_age)
        courses = courses.filter(start_age__lte=max_age)
        courses = courses.filter(end_age__gte=max_age)
    exact_age = request.GET.get('exact_age')
    if exact_age:
        courses = courses.filter(start_age__lte=exact_age)
        courses = courses.filter(end_age__gte=exact_age)
    context = {
        'courses': courses,
        'free_trial_courses': Course.objects.filter(is_free_trial=True) if request.user.is_anonymous or request.user.is_free_trial() else [],
        'tracks': Track.objects.all(),
    }
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        context['min_age'] = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        context['max_age'] = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
    return render(template_name=f'masterstudy/courses{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)

def course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        min_age = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        max_age = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
        if not (course.start_age <= min_age or course.start_age <= max_age and course.end_age >= max_age):
            return redirect('main:home')
    context = {
        'course': course,
        'lessons': Lesson.objects.filter(course_id=course_id).order_by('order'),
    }
    return render(template_name=f'masterstudy/course{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)


@login_required
@member_required
@students_required
def start(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    course = topic.lesson.course
    if not request.user.is_anonymous and request.user.is_authenticated and request.user.is_member() and request.user.has_students():
        min_age = datetime.now().year - request.user.students.order_by('-birth_year').first().birth_year
        max_age = datetime.now().year - request.user.students.order_by('birth_year').first().birth_year
        if not (course.start_age <= min_age or course.start_age <= max_age and course.end_age >= max_age):
            return redirect('main:home')
    help_slots = {}
    for i in range(5):
        i_date = timezone.now().date() + timedelta(days=i)
        help_slots[i_date] = []
        periods = Period.objects.filter(start_date__lte=i_date, end_date__gte=i_date, courses=course)
        for period in periods:
            time = period.start_time
            while time < period.end_time:
                toggle = True
                if HelpSession.objects.filter(user=request.user, teacher=period.user, date=i_date, time=time).exists():
                    toggle = False
                help_slots[i_date] += [{'time': time.strftime('%H:%M'), 'open': toggle}]
                time = (datetime.combine(date(1,1,1), time) + timedelta(minutes=30)).time()

    prev_lesson = Lesson.objects.filter(course_id=course, order=topic.lesson.order-1).first()
    next_lesson = Lesson.objects.filter(course_id=course, order=topic.lesson.order+1).first()
    prev_topic = (Topic.objects.filter(lesson__course_id=course, lesson=topic.lesson, order=topic.order-1).first() or
                       (prev_lesson.topics.all().last() if prev_lesson else None))
    if prev_topic and not prev_topic.completed():
        return redirect('course:start', topic_id=prev_topic.id)
    context = {
        'course': course,
        'lessons': Lesson.objects.filter(course_id=course).order_by('order'),
        'topic': topic,
        'prev_topic': prev_topic,
        'next_topic': (Topic.objects.filter(lesson__course_id=course, lesson=topic.lesson, order=topic.order+1).first() or
                       (next_lesson.topics.all().first() if next_lesson else None)),
        'help_slots': help_slots,
    }
    # TODO(gaytomycode): if there is no more topics then let's go to the cert gen
    return render(template_name=f'masterstudy/lesson{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)


@login_required
@member_required
@students_required
def mark_complete(request):
    topic_id = request.POST['topic']
    Progress.objects.get_or_create(user=request.user, std_id=request.COOKIES['std_id'], topic_id=topic_id)
    return redirect('course:start', topic_id=topic_id)

@login_required
@member_required
@students_required
def answer_mcq(request, quiz_id):
    choice = request.POST['choice']
    quiz = MCQQuiz.objects.get(id=quiz_id)
    _, _ = MCQQuizSolution.objects.get_or_create(user=request.user, std_id=request.COOKIES['std_id'], mcq_quiz=quiz, defaults={'choice': choice})
    Progress.objects.get_or_create(user=request.user, std_id=request.COOKIES['std_id'], topic_id=quiz.topic_id)
    return redirect('course:start', topic_id=quiz.topic_id)

@login_required
@member_required
@students_required
def answer_tf(request, quiz_id):
    choice = request.POST['choice']
    quiz = TFQuiz.objects.get(id=quiz_id)
    _, _ = TFQuizSolution.objects.get_or_create(user=request.user, std_id=request.COOKIES['std_id'], tf_quiz=quiz, defaults={'choice': True if choice == 'true' else False})
    Progress.objects.get_or_create(user=request.user, std_id=request.COOKIES['std_id'], topic_id=quiz.topic_id)
    return redirect('course:start', topic_id=quiz.topic_id)


@login_required
@free_trial_required
def free_trial_start(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    course = topic.lesson.course
    if not (not request.user.is_anonymous and request.user.is_authenticated and request.user.is_free_trial()):
        return redirect('main:home')
    help_slots = {}
    for i in range(5):
        i_date = timezone.now().date() + timedelta(days=i)
        help_slots[i_date] = []
        periods = Period.objects.filter(start_date__lte=i_date, end_date__gte=i_date, courses=course)
        for period in periods:
            time = period.start_time
            while time < period.end_time:
                toggle = True
                if HelpSession.objects.filter(user=request.user, teacher=period.user, date=i_date, time=time).exists():
                    toggle = False
                help_slots[i_date] += [{'time': time.strftime('%H:%M'), 'open': toggle}]
                time = (datetime.combine(date(1,1,1), time) + timedelta(minutes=30)).time()

    prev_lesson = Lesson.objects.filter(course_id=course, order=topic.lesson.order-1).first()
    next_lesson = Lesson.objects.filter(course_id=course, order=topic.lesson.order+1).first()
    prev_topic = (Topic.objects.filter(lesson__course_id=course, lesson=topic.lesson, order=topic.order-1).first() or
                       (prev_lesson.topics.all().last() if prev_lesson else None))
    if prev_topic and not prev_topic.free_trial_completed():
        return redirect('course:free-trial-start', topic_id=prev_topic.id)
    context = {
        'course': course,
        'lessons': Lesson.objects.filter(course_id=course).order_by('order'),
        'topic': topic,
        'prev_topic': prev_topic,
        'next_topic': (Topic.objects.filter(lesson__course_id=course, lesson=topic.lesson, order=topic.order+1).first() or
                       (next_lesson.topics.all().first() if next_lesson else None)),
        'help_slots': help_slots,
    }
    # TODO(gaytomycode): if there is no more topics then let's go to the cert gen
    return render(template_name=f'masterstudy/trial-lesson{"_ar" if settings.AS_LANG == "ar" else ""}.html', request=request, context=context)


@login_required
@free_trial_required
def free_trial_mark_complete(request):
    topic_id = request.POST['topic']
    std = Student.objects.get(user=request.user, name='Trial Student')
    Progress.objects.get_or_create(user=request.user, std=std, topic_id=topic_id)

    topic = Topic.objects.get(id=topic_id)
    next_lesson = Lesson.objects.filter(course_id=topic.lesson.course, order=topic.lesson.order+1).first()
    next_topic = (Topic.objects.filter(lesson__course_id=topic.lesson.course, lesson=topic.lesson, order=topic.order+1).first() or
                  (next_lesson.topics.all().first() if next_lesson else None))
    if next_topic:
        return redirect('course:free-trial-start', topic_id=next_topic.id)
    else:
        cert_id = f'{topic.lesson.course.id}-{std.id}'
        return redirect('main:cert', cert_id=cert_id)


@login_required
@free_trial_required
def free_trial_answer_mcq(request, quiz_id):
    choice = request.POST['choice']
    quiz = MCQQuiz.objects.get(id=quiz_id)
    std = Student.objects.get(user=request.user, name='Trial Student')
    _, _ = MCQQuizSolution.objects.get_or_create(user=request.user, std=std, mcq_quiz=quiz, defaults={'choice': choice})
    Progress.objects.get_or_create(user=request.user, std=std, topic_id=quiz.topic_id)
    return redirect('course:free-trial-start', topic_id=quiz.topic_id)

@login_required
@free_trial_required
def free_trial_answer_tf(request, quiz_id):
    choice = request.POST['choice']
    quiz = TFQuiz.objects.get(id=quiz_id)
    std = Student.objects.get(user=request.user, name='Trial Student')
    _, _ = TFQuizSolution.objects.get_or_create(user=request.user, std=std, tf_quiz=quiz, defaults={'choice': True if choice == 'true' else False})
    Progress.objects.get_or_create(user=request.user, std=std, topic_id=quiz.topic_id)
    return redirect('course:free-trial-start', topic_id=quiz.topic_id)
