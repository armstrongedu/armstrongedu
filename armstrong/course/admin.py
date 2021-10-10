from django.contrib import admin
from django.forms import widgets, TextInput
from django.db import models

from .models import Category, Track, Course, Lesson, Topic, Text, Video, MCQQuiz, TFQuiz, Game, Progress, MCQQuizSolution, TFQuizSolution


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class CourseInline(admin.TabularInline):
    model = Course
    raw_id_fields = ('track',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    inlines = (CourseInline,)


class LessonInline(admin.TabularInline):
    model = Lesson
    raw_id_fields = ('course',)


@admin.register(Course)
class CouresAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title',)
    inlines = (LessonInline,)


class TopicInline(admin.TabularInline):
    model = Topic
    raw_id_fileds = ('lesson',)


class TextInline(admin.TabularInline):
    model = Text
    raw_id_fileds = ('lesson',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'topic':
            lesson_id = request.resolver_match.kwargs.get('object_id')
            field.queryset = field.queryset.filter(lesson=lesson_id, type=Topic.TEXT,)
        return field


class GameInline(admin.TabularInline):
    model = Game
    raw_id_fileds = ('lesson',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'topic':
            lesson_id = request.resolver_match.kwargs.get('object_id')
            field.queryset = field.queryset.filter(lesson=lesson_id, type=Topic.GAME,)
        return field


class VideoInline(admin.TabularInline):
    model = Video
    raw_id_fileds = ('lesson',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'topic':
            lesson_id = request.resolver_match.kwargs.get('object_id')
            field.queryset = field.queryset.filter(lesson=lesson_id, type=Topic.VIDEO,)
        return field


class MCQQuizInline(admin.TabularInline):
    model = MCQQuiz
    raw_id_fileds = ('lesson',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'topic':
            lesson_id = request.resolver_match.kwargs.get('object_id')
            field.queryset = field.queryset.filter(lesson=lesson_id, type=Topic.QUIZ,)
        return field


class TFQuizInline(admin.TabularInline):
    model = TFQuiz
    raw_id_fileds = ('lesson',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'topic':
            lesson_id = request.resolver_match.kwargs.get('object_id')
            field.queryset = field.queryset.filter(lesson=lesson_id, type=Topic.QUIZ,)
        return field


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    search_fields = (lambda s: s.__str__(), 'title', 'summary',)
    list_display = (lambda s: s.__str__(), 'title',)
    list_filter = ('course',)
    inlines = (TopicInline, TextInline, GameInline, VideoInline, MCQQuizInline, TFQuizInline,)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'std', 'topic')
    search_fields = ('user', 'std', 'topic',)


@admin.register(MCQQuizSolution)
class MCQQuizSolutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'std', 'mcq_quiz', 'choice')
    search_fields = ('user', 'std', 'mcq_quiz', 'choice')


@admin.register(TFQuizSolution)
class TFQuizSolutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'std', 'tf_quiz', 'choice')
    search_fields = ('user', 'std', 'tf_quiz', 'choice')
