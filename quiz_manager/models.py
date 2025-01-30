from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .util import cut


class Quiz(models.Model):
    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizzes')

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @admin.display
    def questions_count(self) -> int:
        return self.question_set.count()

    def __str__(self):
        questions_count = self.question_set.count()
        title = cut(self.title)
        if questions_count == 1:
            return f'{title} ({questions_count} questão)'
        return f'{title} ({questions_count} questões)'


class Question(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'E', _('Easy')
        MEDIUM = 'M', _('Medium')
        HARD = 'H', _('Hard')

    text = models.TextField(null=False, blank=False, help_text='Texto da pergunta')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=1, choices=Difficulty, default=Difficulty.EASY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return cut(self.text)


class Answer(models.Model):
    text = models.TextField(null=False, default='', help_text='Texto da opção de resposta')
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return cut(self.text)

    def clean(self):
        super().clean()
        if not self.is_correct:
            if not Answer.objects.filter(question=self.question, is_correct=True).exclude(id=self.id).exists():
                raise ValidationError("At least one answer must be marked as correct for the question.")

    def save(self, *args, **kwargs):
        if self.is_correct:
            Answer.objects.filter(question=self.question).exclude(id=self.id).update(is_correct=False)
        super().save(*args, **kwargs)
