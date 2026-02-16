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
    search_fields = ['question_text']  # Можно добавить для улучшения

# LessonAdmin с QuestionInline и всеми атрибутами
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']
    list_filter = ['course']  # ✅ Это уже есть!
    search_fields = ['title']  # Можно добавить поиск по названию
    ordering = ['course', 'order']  # Сортировка

# Регистрируем все модели
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
