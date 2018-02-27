# Generated by Django 2.0.2 on 2018-02-14 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0003_auto_20180214_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='isValidated',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='extraTime',
            field=models.CharField(choices=[('0', '0'), ('2', '2'), ('3', '3')], default='2hr', max_length=100),
        ),
    ]
