# Generated by Django 5.1.3 on 2025-02-01 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_manager', '0006_remove_answer_is_correct_question_correct_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
