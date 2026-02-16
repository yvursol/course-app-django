from django.urls import path
from . import views

urlpatterns = [
    # Course details page
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    
    # Submit answer for a question
    path('question/<int:question_id>/submit/', views.submit, name='submit'),
    
    # Show exam results
    path('course/<int:course_id>/results/', views.show_exam_result, name='show_exam_result'),
]
