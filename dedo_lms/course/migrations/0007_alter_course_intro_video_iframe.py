# Generated by Django 3.2.3 on 2021-09-10 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_course_intro_video_iframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='intro_video_iframe',
            field=models.TextField(),
        ),
    ]