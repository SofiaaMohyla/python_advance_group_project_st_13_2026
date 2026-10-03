from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import StudentGrade


class StudentGradeTests(TestCase):
    def test_create_grade_for_student(self):
        student = get_user_model().objects.create_user(username='student', password='Qwerty123!')

        grade = StudentGrade.objects.create(
            student=student,
            subject='Математика',
            grade=12,
            comment='Відмінно.'
        )

        self.assertEqual(grade.student, student)
        self.assertEqual(grade.subject, 'Математика')
        self.assertEqual(grade.grade, 12)
        self.assertIn('Відмінно', grade.comment)
        self.assertTrue(str(grade).startswith('student'))
