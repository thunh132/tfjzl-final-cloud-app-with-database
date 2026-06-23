from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# Hàm xử lý khi học viên bấm nút nộp bài (Submit)
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Thu thập tất cả các ID đáp án mà người dùng đã tích chọn
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))
        
        # Tính toán điểm số
        total_score = 0
        questions = course.question_set.all()
        for question in questions:
            if question.is_get_score(selected_choice_ids):
                total_score += question.grade
                
        # Lưu kết quả tạm thời vào session để hiển thị ở trang kết quả
        request.session['total_score'] = total_score
        return redirect('onlinecourse:show_exam_result', course_id=course.id)
        
    return HttpResponseRedirect(reverse('onlinecourse:index'))

# Hàm hiển thị kết quả thi (Show Exam Result)
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    total_score = request.session.get('total_score', 0)
    
    # Giả lập điểm tối đa của bài thi là 10 để tính phần trăm đạt được
    max_score = sum([q.grade for q in course.question_set.all()]) or 10
    percentage = (total_score / max_score) * 100
    
    context = {
        'course': course,
        'total_score': total_score,
        'max_score': max_score,
        'percentage': percentage,
        'passed': percentage >= 70
    }
    # Render ra một giao diện kết quả nhỏ để phục vụ việc chụp ảnh Task 7
    return render(request, 'onlinecourse/exam_result.html', context)