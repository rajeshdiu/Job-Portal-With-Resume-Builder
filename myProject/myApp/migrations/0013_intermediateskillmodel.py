# Generated by Django 5.1.1 on 2024-09-21 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0012_skillmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntermediateSkillModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('My_Skill_Name', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
