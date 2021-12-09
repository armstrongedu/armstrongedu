# Generated by Django 3.2.3 on 2021-12-09 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_auto_20211028_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiptype',
            name='plan',
            field=models.IntegerField(choices=[(0, 'Basic Plan'), (1, 'Plus Plan')], default=1),
            preserve_default=False,
        ),
    ]