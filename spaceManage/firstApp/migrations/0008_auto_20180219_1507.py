# Generated by Django 2.0.2 on 2018-02-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0007_auto_20180219_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='notes',
            field=models.CharField(max_length=500),
        ),
    ]
