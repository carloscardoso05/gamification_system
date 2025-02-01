from django.contrib import admin
from django.db import models
from django.db.models.aggregates import Count
from django.forms import Textarea

from .models import Quiz, Question, Answer
from .util import cut


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    max_num = 4
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 3, 'cols': 60}),
        }
    }


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'questions_count', 'is_private', 'created_at', 'updated_at']
    list_editable = ['title', 'is_private']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(questions_count=Count('question'))
        return queryset

    def questions_count(self, obj):
        return obj.questions_count

    questions_count.admin_order_field = 'questions_count'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'formatted_text', 'difficulty', 'quiz', 'created_at', 'updated_at']
    inlines = [AnswerInline]

    @admin.display(ordering='text', description='Answer text')
    def formatted_text(self, obj: Question) -> str:
        return cut(obj.text)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'is_correct', 'question', 'created_at', 'updated_at']
    list_editable = ['text', 'is_correct']

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 3, 'cols': 60}),
        }
    }
