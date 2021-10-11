from django.shortcuts import render
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from main.utils import localize
from course.models import Topic
from .models import Period, HelpSession


member_required = user_passes_test(lambda user: user.is_member(), login_url='/')
students_required = user_passes_test(lambda user: user.has_students(), login_url='/authorization/add-students/')

@login_required
@member_required
@students_required
def place_help(request):
    topic_id, date, time = request.POST['help'].split('-')
    teachers = [period.user for period in Topic.objects.get(id=topic_id).lesson.course.periods.all()]
    date_time = datetime.strptime(f'{date} {time}', '%b. %d, %Y %H:%M')
    booked = False
    for teacher in teachers:
        if booked:
            break
        _, created = HelpSession.objects.get_or_create(
            user=request.user,
            teacher=teacher,
            date=date_time.date(),
            time=date_time.time(),
            defaults={
                'help_text': request.POST.get('help_text'),
            }
        )
        if created:
            booked = True
    return redirect('course:start', topic_id=topic_id)


@login_required
@member_required
@students_required
def start_help(request, session_id):
    context = { }
    return render(template_name=localize('masterstudy/help_session.html') , request=request, context=context)
