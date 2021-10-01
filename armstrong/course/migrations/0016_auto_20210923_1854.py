# Generated by Django 3.2.3 on 2021-09-23 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_auto_20210923_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='course',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='course.track'),
        ),
    ]