from django.contrib import admin
from .models import Poll, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title", "description")
    inlines = [ChoiceInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "poll", "choice", "voted_at")
    list_filter = ("poll", "choice")