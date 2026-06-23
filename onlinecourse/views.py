from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # 1. Lấy danh sách ID các đáp án mà học viên đã tick chọn từ form
        selected_ids = [int(choice_id) for choice_id in request.POST.getlist('choice')]
        
        # 2. Lấy Enrollment của user hiện tại
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        
        # 3. Tạo một bản ghi Submission để lưu lại lượt làm bài
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(selected_ids)
        submission.save()
        
        # 4. Tính toán điểm số
        total_score = 0
        max_score = 0
        for question in course.question_set.all():
            max_score += question.grade
            if question.is_get_score(selected_ids):
                total_score += question.grade
                
        # Tính phần trăm
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        passed = percentage >= 70

        # 5. Lưu tạm vào session để bên hàm show_exam_result đọc ra hiển thị
        request.session['total_score'] = total_score
        request.session['max_score'] = max_score
        request.session['percentage'] = percentage
        request.session['passed'] = passed

        return redirect(reverse('onlinecourse:show_exam_result', args=(course.id,)))

def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # Đọc dữ liệu đã tính toán từ session ra
    context = {
        'course': course,
        'total_score': request.session.get('total_score', 0),
        'max_score': request.session.get('max_score', 0),
        'percentage': request.session.get('percentage', 0.0),
        'passed': request.session.get('passed', False)
    }
    return render(request, 'onlinecourse/exam_result.html', context)