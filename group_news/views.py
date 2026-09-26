from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import News

class NewsListView(PermissionRequiredMixin, ListView):
    model = News
    template_name = 'group_news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 3
    permission_required = 'group_news.view_news'

class NewsDetailView(PermissionRequiredMixin, DetailView):
    model = News
    template_name = 'group_news/news_detail.html'
    context_object_name = "news"
    permission_required = 'group_news.view_news'

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = ['title', 'content']
    success_url = reverse_lazy('group_news:news_list')
    template_name = 'group_news/create_news.html'
    permission_required = 'group_news.add_news'

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'group_news/delete_news.html'
    success_url = reverse_lazy('group_news:news_list')
    permission_required = 'group_news.delete_news'