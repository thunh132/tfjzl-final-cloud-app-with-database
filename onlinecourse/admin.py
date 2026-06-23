from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# Cấu hình Choice hiển thị dạng Inline (nằm trong Question)
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

# Cấu hình Question hiển thị dạng Inline (nằm trong Course)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# Cấu hình hiển thị cho Lesson
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']

# Cấu hình hiển thị cho Question kèm theo các Choice của nó
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']

# Cấu hình hiển thị cho Course kèm theo các Question và Lesson
class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# Đăng ký các lớp với trang Admin của Django
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)