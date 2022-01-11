from django.urls import path

from . import views

urlpatterns = [
    path('', views.courses, name='courses'),
    path('mark-complete', views.mark_complete, name='mark-complete'),
    path('free-trial-mark-complete', views.free_trial_mark_complete, name='free-trial-mark-complete'),
    path('start/<topic_id>', views.start, name='start'),
    path('answer-mcq/<quiz_id>', views.answer_mcq, name='answer-mcq'),
    path('answer-tf/<quiz_id>', views.answer_tf, name='answer-tf'),
    path('free-trial-start/<topic_id>', views.free_trial_start, name='free-trial-start'),
    path('free-trial-answer-mcq/<quiz_id>', views.free_trial_answer_mcq, name='free-trial-answer-mcq'),
    path('free-trial-answer-tf/<quiz_id>', views.free_trial_answer_tf, name='free-trial-answer-tf'),
    path('builder', views.builder, name='builder'),
    path('build', views.build, name='build'),
    path('build/<course_id>', views.build, name='build'),
    path('<course_id>', views.course, name='course'),
]
