from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Đường dẫn xử lý khi học viên bấm nút Submit bài thi (Task 5)
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Đường dẫn hiển thị kết quả bài thi sau khi nộp
    path('<int:course_id>/show_exam_result/', views.show_exam_result, name='show_exam_result'),
]