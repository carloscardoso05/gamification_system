from django.db.models.signals import post_save
from django.dispatch import receiver

from quiz_manager.models import Answer


@receiver(post_save, sender=Answer)
def assign_default_correct_answer(instance: Answer, **kwargs):
    answers = Answer.objects.filter(question=instance.question)
    if not answers.filter(is_correct=True).exists():
        default_correct_answer = answers.first()
        default_correct_answer.is_correct = True
        default_correct_answer.save()
