from django.urls import path
from .views import ForumMessageDeleteView, ForumMessageListView, ForumMessageCreateView, ForumMessageDetailView, ForumMessageUpdateView

urlpatterns = [
    path('', ForumMessageListView.as_view(), name='forum_message_list'),
    path('create/', ForumMessageCreateView.as_view(), name='forum_message_create'),
    path('<int:pk>/', ForumMessageDetailView.as_view(), name='forum_message_detail'),
    path('<int:pk>/update/', ForumMessageUpdateView.as_view(), name='forum_message_update'),
    path('<int:pk>/delete/', ForumMessageDeleteView.as_view(), name='forum_message_delete'),
]