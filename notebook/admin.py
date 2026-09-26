from django.contrib import admin
from .models import StudentGrade

@admin.register(StudentGrade)
class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'updated_at_formatted')
    list_filter = ('subject', 'grade')
    search_fields = ('student__username', 'subject', 'comment')

    @admin.display(description='Дата')
    def updated_at_formatted(self, obj):
        return obj.updated_at.strftime('%d.%m.%Y %H:%M')
