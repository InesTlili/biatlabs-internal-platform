# Generated by Django 2.0.2 on 2018-02-19 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0006_auto_20180219_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='notes',
            field=models.CharField(default='Coffee / Kitchen', max_length=500),
        ),
    ]
