import io
import random

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import apivideo
from apivideo.apis import VideosApi
from apivideo.exceptions import ApiAuthException


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

    def __str__(self):
        return self.title


class Course(models.Model):
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    intro_video_iframe = models.FileField(storage=APIVideoStorage(), max_length=1000)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, related_name='lessons')
    title = models.CharField(max_length=255)
    summary = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return f'{self.course} - {self.order}'


class Topic(models.Model):
    TEXT, VIDEO, QUIZ = range(3)
    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (VIDEO, 'Video'),
        (QUIZ, 'Quiz'),
    )
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='topics')
    order = models.IntegerField()
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.lesson.course} - {self.lesson.order}.{self.order}'


class Text(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='texts')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='text')
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='videos')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='video')
    title = models.CharField(max_length=255)
    video_iframe = models.FileField(storage=APIVideoStorage(), max_length=1000)

    def __str__(self):
        return self.title

class MCQQuiz(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='mcq_quizez')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='mcq_quiz')
    question = models.CharField(max_length=255)
    diagram = models.ImageField(null=True, blank=True)
    wrong_choices = ArrayField(models.CharField(max_length=255))
    correct_choice = models.CharField(max_length=255)

    def __str__(self):
        return self.question

    def choices(self):
        choices = [*self.wrong_choices, self.correct_choice]
        random.shuffle(choices)
        return choices

class TFQuiz(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='tf_quizez')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='tf_quiz')
    question = models.CharField(max_length=255)
    diagram = models.ImageField(null=True, blank=True)
    answer = models.BooleanField()

    def __str__(self):
        return self.question
