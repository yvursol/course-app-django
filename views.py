from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Question, Choice, Submission

def course_details(request, course_id):
    """Display course details with all lessons"""
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'myonlinecourse/course_details_bootstrap.html', {'course': course})

@login_required
def submit(request, question_id):
    """Handle exam question submission"""
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        choice_id = request.POST.get('choice')
        
        if choice_id:
            choice = get_object_or_404(Choice, pk=choice_id)
            # Save submission
            submission = Submission.objects.create(
                user=request.user,
                question=question,
                choice=choice
            )
            messages.success(request, 'Answer submitted successfully!')
        else:
            messages.error(request, 'Please select an answer.')
            
    return redirect('course_details', course_id=question.lesson.course.id)

@login_required
def show_exam_result(request, course_id):
    """Display exam results for a course"""
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    questions = Question.objects.filter(lesson__in=lessons)
    
    # Get user's submissions for this course
    submissions = Submission.objects.filter(
        user=request.user,
        question__in=questions
    ).select_related('question', 'choice')
    
    # Calculate score
    total_points = 0
    earned_points = 0
    results = []
    
    for question in questions:
        total_points += question.points
        user_submission = submissions.filter(question=question).first()
        is_correct = False
        
        if user_submission and user_submission.choice.is_correct:
            is_correct = True
            earned_points += question.points
            
        results.append({
            'question': question,
            'submission': user_submission,
            'is_correct': is_correct
        })
    
    score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    
    context = {
        'course': course,
        'results': results,
        'earned_points': earned_points,
        'total_points': total_points,
        'score_percentage': score_percentage
    }
    
    return render(request, 'myonlinecourse/exam_result.html', context)
