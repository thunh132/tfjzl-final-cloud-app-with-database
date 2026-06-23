from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Enrollment, Instructor, Learner

# 1. Định nghĩa ChoiceInline để quản lý Choice ngay trong Question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

# 2. Định nghĩa LessonInline để quản lý Lesson ngay trong Course
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

# 3. Định nghĩa QuestionInline để quản lý Question ngay trong Course
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

# 4. Định nghĩa cấu hình Admin cho Course
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# 5. Định nghĩa cấu hình Admin cho Question
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'grade')
    search_fields = ['question_text']

# 6. Định nghĩa cấu hình Admin cho Lesson
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']

# Đăng ký toàn bộ 7 class vào Admin Site để chấm điểm
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)
admin.site.register(Instructor)
admin.site.register(Learner)