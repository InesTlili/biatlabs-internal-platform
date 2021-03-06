# Generated by Django 2.0.2 on 2018-02-20 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0008_auto_20180219_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoURL', models.URLField()),
                ('articleURL', models.URLField()),
                ('textContent', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('isActive', models.BooleanField(default=False)),
                ('activationDate', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.Module'),
        ),
        migrations.AddField(
            model_name='content',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firstApp.Course'),
        ),
    ]
