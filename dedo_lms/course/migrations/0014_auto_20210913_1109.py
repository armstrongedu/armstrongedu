# Generated by Django 3.2.3 on 2021-09-13 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20210913_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tfquiz',
            name='false_choice',
        ),
        migrations.RemoveField(
            model_name='tfquiz',
            name='true_choices',
        ),
        migrations.AddField(
            model_name='tfquiz',
            name='answer',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mcqquiz',
            name='topic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mcq_quiz', to='course.topic'),
        ),
        migrations.AlterField(
            model_name='text',
            name='topic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text', to='course.topic'),
        ),
        migrations.AlterField(
            model_name='tfquiz',
            name='topic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tf_quiz', to='course.topic'),
        ),
        migrations.AlterField(
            model_name='video',
            name='topic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video', to='course.topic'),
        ),
    ]