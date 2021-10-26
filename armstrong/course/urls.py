from django.urls import path

from . import views

urlpatterns = [
    path('', views.courses, name='courses'),
    path('mark-complete', views.mark_complete, name='mark-complete'),
    path('<course_id>', views.course, name='course'),
    path('start/<topic_id>', views.start, name='start'),
    path('answer-mcq/<quiz_id>', views.answer_mcq, name='answer-mcq'),
    path('answer-tf/<quiz_id>', views.answer_tf, name='answer-tf'),
]
