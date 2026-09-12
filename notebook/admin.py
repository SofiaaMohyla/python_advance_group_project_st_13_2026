from django.contrib import admin
from .models import StudentGrade

@admin.register(StudentGrade)
class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'updated_at')
    list_filter = ('subject', 'grade')
    search_fields = ('student__username', 'subject', 'comment')
