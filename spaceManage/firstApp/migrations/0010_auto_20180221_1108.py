# Generated by Django 2.0.2 on 2018-02-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0009_auto_20180220_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='articleURL',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='textContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='videoURL',
            field=models.URLField(blank=True, null=True),
        ),
    ]
