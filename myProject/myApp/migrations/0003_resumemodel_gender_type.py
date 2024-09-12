# Generated by Django 5.1.1 on 2024-09-12 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_resumemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumemodel',
            name='gender_type',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=200, null=True),
        ),
    ]