from django.urls import path

from .views import StudentGradeCreateView, StudentGradeDeleteView, StudentGradeListView, StudentGradeUpdateView

urlpatterns = [
    path('', StudentGradeListView.as_view(), name='notebook_list'),
    path('new/', StudentGradeCreateView.as_view(), name='notebook_create'),
    path('<int:pk>/edit/', StudentGradeUpdateView.as_view(), name='notebook_update'),
    path('<int:pk>/delete/', StudentGradeDeleteView.as_view(), name='notebook_delete'),
]
