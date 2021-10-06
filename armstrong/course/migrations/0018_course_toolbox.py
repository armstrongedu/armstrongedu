# Generated by Django 3.2.3 on 2021-10-03 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('toolbox', '0004_remove_toolbox_courses'),
        ('course', '0017_course_track_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='toolbox',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='toolbox.toolbox'),
        ),
    ]
