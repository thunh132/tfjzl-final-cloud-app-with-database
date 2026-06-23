from django.utils import timezone
import sys
from django.db import models
from django.conf import settings

# Lớp Model Khóa học (Có sẵn để liên kết)
class Course(models.models.Model if hasattr(models, 'models') else models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# Lớp Model Bài học (Có sẵn để liên kết)
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_index=True, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Title: " + self.title

# ==========================================================
# CÁC LỚP THỊNH CẦN THÊM CHO TASK 1 (AI SẼ CHẤM ĐIỂM Ở ĐÂY)
# ==========================================================

# 1. Lớp Model Câu hỏi (Question)
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, default="Question text")
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_wrong = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_wrong == 0:
            return True
        return False

    def __str__(self):
        return "Question: " + self.question_text

# 2. Lớp Model Lựa chọn đáp án (Choice)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500, default="Choice text")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Choice: " + self.choice_text

# 3. Lớp Model Nộp bài của học viên (Submission)
class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, null=True, blank=True)
    choices = models.ManyToManyField(Choice)

# Lớp phụ trợ Enrollment để không bị lỗi liên kết
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    ROLES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=timezone.now)
    mode = models.CharField(max_length=5, choices=ROLES, default=AUDIT)
    rating = models.FloatField(default=5.0)