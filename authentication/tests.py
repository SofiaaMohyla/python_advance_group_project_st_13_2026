from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from events_calendar.models import Event


User = get_user_model()


class EventPermissionsTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user', password='password')
		self.manager = User.objects.create_user(
			username='manager', password='password', role='moderator'
		)
		self.event = Event.objects.create(
			title='Початкова подія',
			description='Опис',
			start_time='2026-10-01T00:00:00Z',
			end_time='2026-10-02T00:00:00Z',
		)

	def test_regular_user_can_view_events_but_cannot_manage_them(self):
		self.client.login(username='user', password='password')

		view_response = self.client.get(reverse('events'))
		create_response = self.client.get(reverse('create_event'))
		edit_response = self.client.get(reverse('edit_event'))

		self.assertEqual(view_response.status_code, 200)
		self.assertNotContains(view_response, 'Створити подію')
		self.assertEqual(create_response.status_code, 403)
		self.assertEqual(edit_response.status_code, 403)

	def test_manager_can_create_and_edit_events(self):
		self.client.login(username='manager', password='password')

		create_response = self.client.post(reverse('create_event'), {
			'title': 'Нова подія',
			'description': 'Новий опис',
			'start_time': '2026-11-01',
			'end_time': '2026-11-02',
			'location': 'Аудиторія',
		})
		self.assertEqual(create_response.status_code, 200)
		self.assertTrue(Event.objects.filter(title='Нова подія').exists())

		edit_response = self.client.post(reverse('edit_event'), {
			'event_id': self.event.id,
			'title': 'Оновлена подія',
			'description': 'Оновлений опис',
			'location': 'Онлайн',
		})
		self.assertEqual(edit_response.status_code, 302)
		self.event.refresh_from_db()
		self.assertEqual(self.event.title, 'Оновлена подія')
		self.assertEqual(self.event.location, 'Онлайн')

	def test_manager_event_list_is_paginated(self):
		self.client.login(username='manager', password='password')
		for event_number in range(11):
			Event.objects.create(
				title=f'Подія {event_number}',
				description='Опис',
				start_time='2026-10-01T00:00:00Z',
				end_time='2026-10-02T00:00:00Z',
			)

		first_page = self.client.get(reverse('edit_event'))
		second_page = self.client.get(reverse('edit_event'), {'page': 2})

		self.assertEqual(first_page.context['events'].paginator.num_pages, 2)
		self.assertEqual(len(first_page.context['events']), 10)
		self.assertEqual(len(second_page.context['events']), 2)

	def test_regular_user_cannot_change_role_in_profile(self):
		self.client.login(username='user', password='password')

		response = self.client.post(reverse('profile'), {
			'username': 'user',
			'email': '',
			'first_name': '',
			'last_name': '',
			'role': 'admin',
		})

		self.assertEqual(response.status_code, 302)
		self.user.refresh_from_db()
		self.assertEqual(self.user.role, 'user')

	def test_admin_can_change_own_role_in_profile(self):
		admin = User.objects.create_user(
			username='admin', password='password', role='admin'
		)
		self.client.login(username='admin', password='password')

		response = self.client.post(reverse('profile'), {
			'username': 'admin',
			'email': '',
			'first_name': '',
			'last_name': '',
			'role': 'moderator',
		})

		self.assertEqual(response.status_code, 302)
		admin.refresh_from_db()
		self.assertEqual(admin.role, 'moderator')

# Create your tests here.
