from django.urls import path
from .views import NewsListView, NewsDetailView, NewsCreateView, NewsDeleteView

app_name ='group_news'

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete')
]