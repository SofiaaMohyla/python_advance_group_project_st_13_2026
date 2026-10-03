from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PollForm
from .models import Poll, Choice, Vote


# --------------------------------------------------
# Проверка прав администратора / модератора
# --------------------------------------------------

def can_manage_poll(user):
    return user.is_staff or user.is_superuser


# --------------------------------------------------
# Список голосований
# --------------------------------------------------

@login_required
def poll_list(request):
    polls = Poll.objects.all().order_by("-created_at")

    return render(
        request,
        "mypolls/poll_list.html",
        {
            "polls": polls
        }
    )


# --------------------------------------------------
# Создание голосования
# --------------------------------------------------

@login_required
@user_passes_test(can_manage_poll)
def poll_create(request):

    if request.method == "POST":

        form = PollForm(request.POST)

        if form.is_valid():

            poll = form.save(commit=False)

            poll.created_by = request.user

            poll.save()

            choices_text = form.cleaned_data["choices"]

            for choice_text in choices_text.splitlines():

                choice_text = choice_text.strip()

                if choice_text:

                    Choice.objects.create(
                        poll=poll,
                        text=choice_text
                    )

            return redirect("poll_list")

    else:

        form = PollForm()

    return render(
        request,
        "mypolls/poll_create.html",
        {
            "form": form
        }
    )


# --------------------------------------------------
# Просмотр голосования + голосование
# --------------------------------------------------

@login_required
def poll_detail(request, poll_id):

    poll = get_object_or_404(
        Poll,
        id=poll_id
    )

    current_vote = Vote.objects.filter(
        user=request.user,
        poll=poll
    ).first()

    error = None

    if request.method == "POST":

        choice_id = request.POST.get("choice")

        if not choice_id:

            error = "Оберіть один із варіантів відповіді."

        else:

            choice = get_object_or_404(
                Choice,
                id=choice_id,
                poll=poll
            )

            # Если голос уже существует —
            # изменяем его.
            # Если нет — создаём.
            Vote.objects.update_or_create(
                user=request.user,
                poll=poll,
                defaults={
                    "choice": choice
                }
            )

            return redirect(
                "poll_results",
                poll_id=poll.id
            )

    return render(
        request,
        "mypolls/poll_detail.html",
        {
            "poll": poll,
            "current_vote": current_vote,
            "error": error
        }
    )


# --------------------------------------------------
# Результаты
# --------------------------------------------------

@login_required
def poll_results(request, poll_id):

    poll = get_object_or_404(
        Poll,
        id=poll_id
    )

    results = []

    for choice in poll.choices.all():

        votes_count = Vote.objects.filter(
            poll=poll,
            choice=choice
        ).count()

        results.append(
            {
                "choice": choice,
                "votes": votes_count
            }
        )

    total_votes = Vote.objects.filter(
        poll=poll
    ).count()

    return render(
        request,
        "mypolls/poll_results.html",
        {
            "poll": poll,
            "results": results,
            "total_votes": total_votes
        }
    )


# --------------------------------------------------
# Редактирование
# --------------------------------------------------

@login_required
@user_passes_test(can_manage_poll)
def poll_edit(request, poll_id):

    poll = get_object_or_404(
        Poll,
        id=poll_id
    )

    if request.method == "POST":

        form = PollForm(
            request.POST,
            instance=poll
        )

        if form.is_valid():

            form.save()

            # Удаляем старые варианты
            poll.choices.all().delete()

            choices_text = form.cleaned_data["choices"]

            # Создаём новые варианты
            for choice_text in choices_text.splitlines():

                choice_text = choice_text.strip()

                if choice_text:

                    Choice.objects.create(
                        poll=poll,
                        text=choice_text
                    )

            return redirect("poll_list")

    else:

        old_choices = "\n".join(
            poll.choices.values_list(
                "text",
                flat=True
            )
        )

        form = PollForm(
            instance=poll,
            initial={
                "choices": old_choices
            }
        )

    return render(
        request,
        "mypolls/poll_edit.html",
        {
            "form": form,
            "poll": poll
        }
    )


# --------------------------------------------------
# Удаление
# --------------------------------------------------

@login_required
@user_passes_test(can_manage_poll)
def poll_delete(request, poll_id):

    poll = get_object_or_404(
        Poll,
        id=poll_id
    )

    if request.method == "POST":

        poll.delete()

        return redirect("poll_list")

    return render(
        request,
        "mypolls/poll_delete.html",
        {
            "poll": poll
        }
    )