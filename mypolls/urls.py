from django.urls import path

from .views import (
    poll_list,
    poll_create,
    poll_detail,
    poll_results,
    poll_edit,
    poll_delete,
)


urlpatterns = [
    # Список голосований
    path(
        "",
        poll_list,
        name="poll_list"
    ),

    # Создание
    path(
        "create/",
        poll_create,
        name="poll_create"
    ),

    # Просмотр и голосование
    path(
        "<int:poll_id>/",
        poll_detail,
        name="poll_detail"
    ),

    # Результаты
    path(
        "<int:poll_id>/results/",
        poll_results,
        name="poll_results"
    ),

    # Редактирование
    path(
        "<int:poll_id>/edit/",
        poll_edit,
        name="poll_edit"
    ),

    # Удаление
    path(
        "<int:poll_id>/delete/",
        poll_delete,
        name="poll_delete"
    ),
]