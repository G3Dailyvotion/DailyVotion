from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
		

def profile_image_path(instance, filename):
	# Generate a unique filename for each user profile picture
	ext = filename.split('.')[-1]
	new_filename = f"user_{instance.user.id}_profile.{ext}"
	return os.path.join('profile_pictures', new_filename)


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	image = models.ImageField(upload_to=profile_image_path, null=True, blank=True)
	bio = models.TextField(blank=True)
	
	def __str__(self):
		return f"Profile: {self.user.username}"
		
	def get_image_url(self):
		# Return uploaded image URL if it exists and file is present; else fallback to default static image
		try:
			if self.image and hasattr(self.image, 'name') and default_storage.exists(self.image.name):
				return self.image.url
		except Exception:
			pass
		return settings.STATIC_URL + 'pictures/Profilepic.jpg'


# Signal to automatically create UserProfile for new users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	"""Create a UserProfile for every new User"""
	if created:
		UserProfile.objects.create(user=instance)


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
