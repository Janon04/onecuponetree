from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Event

class EventModelTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
		self.event = Event.objects.create(
			title='Test Event',
			description='Event description',
			start_date=timezone.now(),
			end_date=timezone.now() + timezone.timedelta(hours=2),
			location='Test Location',
			organizer=self.user,
			status='upcoming',
		)

	def test_event_str(self):
		self.assertIn('Test Event', str(self.event))

	def test_event_status(self):
		self.assertEqual(self.event.status, 'upcoming')


class EventListViewTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='testuser2', password='testpass')
		for i in range(3):
			Event.objects.create(
				title=f'Event {i}',
				description='Description',
				start_date=timezone.now(),
				end_date=timezone.now() + timezone.timedelta(hours=1),
				location='Location',
				organizer=self.user,
				status='upcoming',
			)

	def test_event_list_view(self):
		url = reverse('events:event_list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Event 0')
		self.assertContains(response, 'Event 1')
		self.assertContains(response, 'Event 2')


class EventDetailViewTest(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='testuser3', password='testpass')
		self.event = Event.objects.create(
			title='Detail Event',
			description='Detail description',
			start_date=timezone.now(),
			end_date=timezone.now() + timezone.timedelta(hours=1),
			location='Detail Location',
			organizer=self.user,
			status='upcoming',
		)

	def test_event_detail_view(self):
		url = reverse('events:event_detail', args=[self.event.pk])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Detail Event')

# Create your tests here.
