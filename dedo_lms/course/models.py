from django.db import models
from django.contrib.postgres.fields import ArrayField


class Course(models.Model):
    title = models.CharField(max_length=255)
    intro_video = models.FileField()

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
    VIDEO, QUIZ = range(2)
    TYPE_CHOICES = (
        (VIDEO, 'Video'),
        (QUIZ, 'Quiz'),
    )
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='topics')
    order = models.IntegerField()
    type = models.PositiveIntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.lesson.course} - {self.lesson.order}.{self.order}'


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='videos')
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video = models.FileField()


class MCQQuiz(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='mcq_quizez')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='mcq_quizes')
    question = models.CharField(max_length=255)
    diagram = models.ImageField(null=True, blank=True)
    wrong_choices = ArrayField(models.CharField(max_length=255))
    correct_choice = models.CharField(max_length=255)


class TFQuiz(models.Model):
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, related_name='tf_quizez')
    topic = models.OneToOneField(Topic, null=True, blank=True, on_delete=models.CASCADE, related_name='tf_quizes')
    question = models.CharField(max_length=255)
    diagram = models.ImageField(null=True, blank=True)
    false_choice = ArrayField(models.CharField(max_length=255))
    true_choices = ArrayField(models.CharField(max_length=255))
