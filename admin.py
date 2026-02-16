from django.contrib import admin
# Импортируем ВСЕ 7 классов моделей
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# Inline для Choice внутри Question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Inline для Question внутри Lesson
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2
    show_change_link = True

# QuestionAdmin с ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['id', 'question_text', 'lesson', 'points']
    list_filter = ['lesson']

# LessonAdmin с QuestionInline и list_display
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]  # Добавлено!
    list_display = ['title', 'course', 'order']  # Добавлено!
    list_filter = ['course']

# Регистрируем ВСЕ модели
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)  # С кастомным админом
admin.site.register(Instructor)  # Добавлено!
admin.site.register(Learner)     # Добавлено!
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
