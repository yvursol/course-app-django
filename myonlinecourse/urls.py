from django.urls import path
from . import views

urlpatterns = [
    # Course details page
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    
    # Submit answer for a question
    path('course/<int:course_id>/submit/', views.submit, name='submit'),  # Изменено: используем course_id
    
    # Show exam results
    path('course/<int:course_id>/result/', views.show_exam_result, name='show_exam_result'),  # Изменено: result вместо results
]
