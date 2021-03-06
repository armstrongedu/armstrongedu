# Generated by Django 3.2.3 on 2021-08-07 15:37

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCQQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('diagram', models.ImageField(blank=True, null=True, upload_to='')),
                ('wrong_choices', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('correct_choice', models.CharField(max_length=255)),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mcq_quizez', to='course.lesson')),
                ('topic', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mcq_quizes', to='course.topic')),
            ],
        ),
        migrations.CreateModel(
            name='TFQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('diagram', models.ImageField(blank=True, null=True, upload_to='')),
                ('false_choice', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('true_choices', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), size=None)),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tf_quizez', to='course.lesson')),
                ('topic', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tf_quizes', to='course.topic')),
            ],
        ),
        migrations.DeleteModel(
            name='ImageWrongQuiz',
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]
