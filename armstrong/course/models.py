import io
import random

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import get_user_model

import apivideo
from apivideo.apis import VideosApi
from apivideo.exceptions import ApiAuthException

from django_middleware_global_request.middleware import get_request

from bostaSDK.apiClient import ApiClient
from bostaSDK import delivery
from bostaSDK import pickup
from bostaSDK.utils import Receiver, Address, ContactPerson, DeliveryTypes

import requests

from authorization.models import Student
from toolbox.models import ToolBox


class APIVideoStorage(FileSystemStorage):
    def _save(self, name, content):
        api_key = settings.API_VIDEO_KEY
        with apivideo.AuthenticatedApiClient(api_key) as client:
            videos_api = VideosApi(client)
            video_create_payload = {
                "title": name,
                "description": "",
                "public": True,
                "mp4_support": False,
                "tags": []
            }
            response = videos_api.create(video_create_payload)
            video_id = response["video_id"]
            binary_file = io.BytesIO(content.read())
            binary_file.name = name
            video_response = videos_api.upload(video_id, binary_file)
            iframe = iframe = response['assets']['iframe']
        return iframe

    def get_available_name(self, name, max_length=None):
        return name



class Category(models.Model):
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Course(models.Model):
    TB_NO, TB_GET, TB_PLACED, TB_PICKEDUP, TB_DELIVERY, TB_BOUGHT = range(1, 7)
    category = models.ManyToManyField(Category)
    toolbox = models.ForeignKey(ToolBox, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')
    track = models.ForeignKey(Track, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')
    track_order = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)
    cover = models.ImageField(null=False, blank=False)
    intro_video_iframe = models.FileField(storage=APIVideoStorage(), max_length=1000, null=True, blank=True)
    intro_video_iframe_ar = models.FileField(storage=APIVideoStorage(), max_length=1000, null=True, blank=True)
    start_age = models.IntegerField(null=False, blank=False)
    end_age = models.IntegerField(null=False, blank=False)
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    is_free_trial = models.BooleanField(null=False, blank=False, default=False)
    description = models.TextField(null=False, blank=True, default='')
    description_ar = models.TextField(null=False, blank=True, default='')

    def __str__(self):
        return self.title

    def toolbox_status(self):
        if not self.toolbox:
            return self.TB_NO

        user = get_request().user
        order = user.orders.filter(toolbox=self.toolbox)

        if not order.exists():
            return self.TB_GET

        order = order.first()

        api_client=ApiClient(settings.BOSTA_API_KEY)

        headers = {
            'X-Requested-By': 'python-sdk',
            'Authorization': api_client.apiKey,
        }
        tracking_num = requests.get(f'https://app.bosta.co/api/v0/deliveries/{order.bosta_id}', headers=headers).json()['trackingNumber']

        order_states = {
            'AVAILABLE_FOR_PICKUP': self.TB_PLACED,
            'TICKET_CREATED': self.TB_PLACED,
            'PACKAGE_RECEIVED': self.TB_PICKEDUP,
            'NOT_YET_SHIPPED': self.TB_PICKEDUP,
            'IN_TRANSIT': self.TB_PICKEDUP,
            'OUT_FOR_DELIVERY': self.TB_DELIVERY,
            'RECEIVED_DELIVERY_LOCATION': self.TB_DELIVERY,
            'DELIVERED': self.TB_BOUGHT,
            'CANCELLED': self.TB_BOUGHT,
            'WAITING_FOR_CUSTOMER_ACTION': self.TB_BOUGHT,
            'DELIVERED_TO_SENDER': self.TB_BOUGHT,
            'DELIVERY_FAILED': self.TB_BOUGHT,

        }
        return order_states.get(requests.get(f'https://tracking.bosta.co/shipments/track/{tracking_num}', headers=headers).json()['CurrentStatus']['state'], self.TB_DELIVERY)

class Lesson(models.Model):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='lessons')
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)
    summary = models.TextField()
    summary_ar = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.course} - {self.order}'


class Topic(models.Model):
    TEXT, GAME, VIDEO, QUIZ = range(4)
    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (GAME, 'Game'),
        (VIDEO, 'Video'),
        (QUIZ, 'Quiz'),
    )
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='topics')
    order = models.IntegerField()
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f'{self.lesson.course} - {self.lesson.order}.{self.order}'

    def completed(self):
        return self.progress.filter(user=get_request().user, std=get_request().COOKIES['std_id']).exists()

    def free_trial_completed(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.progress.filter(user=get_request().user, std=std).exists()

class Text(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='texts')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='text')
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)
    text = models.TextField()
    text_ar = models.TextField()

    def __str__(self):
        return self.title

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='videos')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='video')
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)
    video_iframe = models.FileField(storage=APIVideoStorage(), max_length=1000)
    video_iframe_ar = models.FileField(storage=APIVideoStorage(), max_length=1000)

    def __str__(self):
        return self.title


class Game(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='games')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='game')
    title = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255)
    iframe = models.TextField()
    iframe_ar = models.TextField()

    def __str__(self):
        return self.title


class MCQQuiz(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='mcq_quizez')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='mcq_quiz')
    question = models.CharField(max_length=255)
    question_ar = models.CharField(max_length=255)
    diagram = models.ImageField(null=True, blank=True)
    diagram_ar = models.ImageField(null=True, blank=True)
    wrong_choices = ArrayField(models.CharField(max_length=255))
    wrong_choices_ar = ArrayField(models.CharField(max_length=255))
    correct_choice = models.CharField(max_length=255)
    correct_choice_ar = models.CharField(max_length=255)

    def __str__(self):
        return self.question

    def choices(self):
        choices = [*self.wrong_choices, self.correct_choice]
        random.shuffle(choices)
        return choices

    def answered(self):
        return self.mcq_solution.filter(user=get_request().user, std=get_request().COOKIES['std_id']).exists()

    def answered_correct(self):
        return self.mcq_solution.filter(user=get_request().user, std=get_request().COOKIES['std_id']).first().choice == self.correct_choice

    def get_choice(self):
        return self.mcq_solution.filter(user=get_request().user, std=get_request().COOKIES['std_id']).first().choice

    def free_trial_answered(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.mcq_solution.filter(user=get_request().user, std=std).exists()

    def free_trial_answered_correct(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.mcq_solution.filter(user=get_request().user, std=std).first().choice == self.correct_choice

    def free_trial_get_choice(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.mcq_solution.filter(user=get_request().user, std=std).first().choice

class TFQuiz(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='tf_quizez')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='tf_quiz')
    question = models.CharField(max_length=255)
    question_ar = models.CharField(max_length=255)
    diagram = models.ImageField(null=True, blank=True)
    diagram_ar = models.ImageField(null=True, blank=True)
    answer = models.BooleanField()

    def __str__(self):
        return self.question


    def answered(self):
        return self.tf_solution.filter(user=get_request().user, std=get_request().COOKIES['std_id']).exists()

    def answered_correct(self):
        return self.tf_solution.filter(user=get_request().user, std=get_request().COOKIES['std_id']).first().choice == self.answer

    def get_choice(self):
        return self.tf_solution.filter(user=get_request().user, std=get_request().COOKIES['std_id']).first().choice

    def free_trial_answered(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.tf_solution.filter(user=get_request().user, std=std).exists()

    def free_trial_answered_correct(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.tf_solution.filter(user=get_request().user, std=std).first().choice == self.answer

    def free_trial_get_choice(self):
        std = Student.objects.get(user=get_request().user, name='Trial Student')
        return self.tf_solution.filter(user=get_request().user, std=std).first().choice

class Progress(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='progress')
    std = models.ForeignKey(Student, null=False, blank=False, on_delete=models.CASCADE, related_name='progress')
    topic = models.ForeignKey(Topic, null=False, blank=False, on_delete=models.CASCADE, related_name='progress')


class MCQQuizSolution(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='mcq_solution')
    std = models.ForeignKey(Student, null=False, blank=False, on_delete=models.CASCADE, related_name='mcq_solution')
    mcq_quiz = models.ForeignKey(MCQQuiz, null=False, blank=False, on_delete=models.CASCADE, related_name='mcq_solution')
    choice = models.CharField(max_length=255)


class TFQuizSolution(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.CASCADE, related_name='tf_solution')
    std = models.ForeignKey(Student, null=False, blank=False, on_delete=models.CASCADE, related_name='tf_solution')
    tf_quiz = models.ForeignKey(TFQuiz, null=False, blank=False, on_delete=models.CASCADE, related_name='tf_solution')
    choice = models.BooleanField()
