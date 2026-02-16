from django.contrib import admin
# Import all required models
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# Inline configurations for nested models
class ChoiceInline(admin.TabularInline):
    """Allows editing choices directly within question form"""
    model = Choice
    extra = 3

class QuestionInline(admin.TabularInline):
    """Allows editing questions directly within lesson form"""
    model = Question
    extra = 2
    show_change_link = True

# Custom ModelAdmin classes
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model with inline choices"""
    inlines = [ChoiceInline]
    list_display = ['id', 'question_text', 'lesson', 'points']
    list_filter = ['lesson']

class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model with inline questions"""
    inlines = [QuestionInline]
    list_display = ['title', 'course', 'order']
    list_filter = ['course']

# Register all models with their respective admin classes
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
