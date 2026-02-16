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
            # Save or update submission
            submission, created = Submission.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={'choice': choice}
            )
            messages.success(request, 'Answer submitted successfully!')
        else:
            messages.error(request, 'Please select an answer.')
            
    return redirect('course_details', course_id=question.lesson.course.id)

def is_get_score(question, selected_choice):
    """Check if the selected choice is correct and return points"""
    if selected_choice and selected_choice.is_correct:
        return question.points
    return 0

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
    
    # Create a dictionary of submissions by question id
    submission_dict = {s.question.id: s for s in submissions}
    
    # Calculate score and collect selected IDs
    total_points = 0
    earned_points = 0
    results = []
    selected_ids = {}  # Dictionary to store selected choice IDs per question
    
    for question in questions:
        total_points += question.points
        user_submission = submission_dict.get(question.id)
        selected_choice = user_submission.choice if user_submission else None
        
        # Store selected choice ID
        if selected_choice:
            selected_ids[question.id] = selected_choice.id
        
        # Use the helper function to get score
        score = is_get_score(question, selected_choice)
        earned_points += score
        
        is_correct = (score > 0)
            
        results.append({
            'question': question,
            'submission': user_submission,
            'selected_choice': selected_choice,
            'is_correct': is_correct,
            'score': score
        })
    
    # Calculate grade and possible
    grade = earned_points
    possible = total_points
    score_percentage = (grade / possible * 100) if possible > 0 else 0
    
    context = {
        'course': course,
        'results': results,
        'grade': grade,  # Добавлено
        'possible': possible,  # Добавлено
        'earned_points': earned_points,
        'total_points': total_points,
        'score_percentage': score_percentage,
        'selected_ids': selected_ids,  # Добавлено
    }
    
    return render(request, 'myonlinecourse/exam_result.html', context)
