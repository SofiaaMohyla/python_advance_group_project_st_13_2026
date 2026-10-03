from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator

from .models import ForumMessage
from .forms import ForumMessageForm


def is_moderator(user):
    if user.is_authenticated:
        return user.role == 'moderator' or user.role == 'admin'


class ForumMessageListView(View):
    def get(self, request):
        messages = ForumMessage.objects.all().order_by('-created_at')
        pagination = Paginator(messages, 2)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        return render(
            request,
            'forum/forum_message_list.html',
            {
                'messages': messages,
                'page_obj': page_obj,
                'is_moderator': is_moderator(request.user)
            }
        )


@method_decorator(login_required, name='dispatch')
class ForumMessageCreateView(View):

    def get(self, request):
        form = ForumMessageForm()
        return render(request, 'forum/forum_message_create.html', {'form': form})

    def post(self, request):
        form = ForumMessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()

            return redirect('forum_message_list')

        return render(request, 'forum/forum_message_create.html', {'form': form})


class ForumMessageDetailView(View):

    def get(self, request, pk):
        message = get_object_or_404(ForumMessage, pk=pk)

        return render(
            request,
            'forum/forum_message_detail.html',
            {
                'message': message,
                'is_moderator': is_moderator(request.user)
            }
        )


@method_decorator(login_required, name='dispatch')
class ForumMessageUpdateView(View):

    def get(self, request, pk):
        message = get_object_or_404(ForumMessage, pk=pk)

        if message.author != request.user and not is_moderator(request.user):
            return redirect('forum_message_list')

        form = ForumMessageForm(instance=message)

        return render(
            request,
            'forum/forum_message_update.html',
            {'form': form, 'message': message}
        )

    def post(self, request, pk):
        message = get_object_or_404(ForumMessage, pk=pk)

        if message.author != request.user and not is_moderator(request.user):
            return redirect('forum_message_list')

        form = ForumMessageForm(request.POST, instance=message)

        if form.is_valid():
            form.save()
            return redirect('forum_message_detail', pk=message.pk)

        return render(
            request,
            'forum/forum_message_update.html',
            {'form': form, 'message': message}
        )


@method_decorator(login_required, name='dispatch')
class ForumMessageDeleteView(View):


    def get(self, request, pk):
        message = get_object_or_404(ForumMessage, pk=pk)

        if message.author != request.user and not is_moderator(request.user):
            return redirect('forum_message_list')

        return render(
            request,
            'forum/forum_message_delete.html',
            {'message': message}
        )

    def post(self, request, pk):
        message = get_object_or_404(ForumMessage, pk=pk)

        if message.author == request.user or is_moderator(request.user):
            message.delete()


        return redirect('forum_message_list')
