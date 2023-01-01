from django.contrib import admin
from .models import Question, Choice

#class ChoiceInLine(admin.StackedInline)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    exclude = ['votes']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'pub_date', 'was_published_recently']

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']
    
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
