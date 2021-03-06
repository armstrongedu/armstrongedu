# Generated by Django 3.2.3 on 2021-10-10 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authorization', '0004_auto_20211007_1830'),
        ('course', '0019_auto_20211007_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='TFQuizSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.BooleanField()),
                ('std', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tf_solution', to='authorization.student')),
                ('tf_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tf_solution', to='course.tfquiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tf_solution', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('std', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='authorization.student')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='course.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MCQQuizSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=255)),
                ('mcq_quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_solution', to='course.mcqquiz')),
                ('std', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_solution', to='authorization.student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_solution', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
