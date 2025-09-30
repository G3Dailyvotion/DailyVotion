from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class JournalEntry(TimeStampedModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
	date = models.DateField()
	scripture = models.TextField(blank=True)
	observation = models.TextField(blank=True)
	application = models.TextField(blank=True)
	prayer = models.TextField(blank=True)

	class Meta:
		ordering = ['-date', '-created_at']

	def __str__(self):
		return f"JournalEntry({self.user.username}, {self.date})"


class PrayerRequest(TimeStampedModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prayer_requests')
	text = models.TextField()
	status = models.CharField(max_length=32, default='submitted')
	admin_response = models.TextField(blank=True)
	responded_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"PrayerRequest({self.user.username}, {self.created_at.date()})"


class Reflection(TimeStampedModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reflections')
	text = models.TextField()

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"Reflection({self.user.username}, {self.created_at.date()})"


class Feedback(TimeStampedModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
	text = models.TextField()

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		u = self.user.username if self.user else 'anon'
		return f"Feedback({u}, {self.created_at.date()})"
