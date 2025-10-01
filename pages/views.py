def gallery(request):
	return render(request, 'pages/gallery.html')
# --- SOAP Journal Entries page ---
def journalentries(request):
	# Mock data for demonstration
	entries = [
		{
			'date': '2025-09-29',
			'scripture': 'John 3:16',
			'observation': 'God loves the world and gave His Son.',
			'application': 'Trust in God’s love and share it with others.',
			'prayer': 'Thank you Lord for your love. Help me to love others.'
		},
		{
			'date': '2025-09-28',
			'scripture': 'Psalm 23:1',
			'observation': 'The Lord is my shepherd, I lack nothing.',
			'application': 'Rely on God’s guidance daily.',
			'prayer': 'Lead me, Lord, in every step I take.'
		},
		{
			'date': '2025-09-27',
			'scripture': 'Philippians 4:13',
			'observation': 'I can do all things through Christ.',
			'application': 'Face challenges with faith in Christ’s strength.',
			'prayer': 'Give me strength for today’s tasks.'
		},
	]
	return render(request, 'pages/journalentries.html', {'entries': entries})
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .forms import JournalEntryForm, PrayerRequestForm, ReflectionForm, FeedbackForm, ProfileForm
from .models import JournalEntry, PrayerRequest, Reflection, Feedback, UserProfile


def home(request):
	return render(request, 'pages/home.html', { 'now': now() })


def about(request):
	return render(request, 'pages/about.html')


def login_view(request):
	if request.method == 'POST':
		identifier = request.POST.get('identifier', '').strip()
		password = request.POST.get('password', '')
		user = None
		# Try username first
		if identifier:
			user = authenticate(request, username=identifier, password=password)
			if user is None:
				# Try email fallback
				try:
					u = User.objects.get(email__iexact=identifier)
					user = authenticate(request, username=u.username, password=password)
				except User.DoesNotExist:
					user = None
		if user is not None:
			login(request, user)
			return redirect('profile')
		messages.error(request, 'Invalid credentials. Please try again.')
	return render(request, 'pages/login.html')


def register(request):
	if request.method == 'POST':
		full_name = request.POST.get('full_name', '').strip()
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		password1 = request.POST.get('password1', '')
		password2 = request.POST.get('password2', '')

		# Basic validations
		if not username or not password1 or not password2:
			messages.error(request, 'Please fill in all required fields.')
			return render(request, 'pages/register.html')
		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			return render(request, 'pages/register.html')
		if User.objects.filter(username__iexact=username).exists():
			messages.error(request, 'This username is already taken.')
			return render(request, 'pages/register.html')
		if email and User.objects.filter(email__iexact=email).exists():
			messages.error(request, 'An account with this email already exists.')
			return render(request, 'pages/register.html')

		first_name = ''
		last_name = ''
		if full_name:
			parts = full_name.split()
			first_name = parts[0]
			last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

		user = User.objects.create_user(
			username=username,
			email=email,
			password=password1,
			first_name=first_name,
			last_name=last_name,
		)
		
		# Create UserProfile for the new user
		UserProfile.objects.create(user=user)
		
		login(request, user)
		return redirect('profile')

	return render(request, 'pages/register.html')

def profile(request):
	if not request.user.is_authenticated:
		# Provide dummy data for design preview
		class DummyUser:
			username = 'demo_user'
			def get_full_name(self): return 'Demo User'
		request.user = DummyUser()
		recent_post = None
		recent_prayers = []
		class MockReflection:
			def __init__(self, text, created_at):
				self.text = text
				self.created_at = created_at
		recent_reflections = [
			MockReflection('Today I learned to trust God more and worry less.', '2025-09-29'),
			MockReflection('Grateful for the blessings I have and the people around me.', '2025-09-28')
		]
	else:
		# Ensure a UserProfile exists for authenticated users (older accounts may be missing one)
		try:
			UserProfile.objects.get_or_create(user=request.user)
		except Exception:
			# If something odd happens, continue gracefully; template falls back to default avatar
			pass
		recent_post = JournalEntry.objects.filter(user=request.user).order_by('-date', '-created_at').first()
		recent_prayers = PrayerRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
		recent_reflections = Reflection.objects.filter(user=request.user).order_by('-created_at')[:5]
	return render(request, 'pages/profile.html', {
		'recent_post': recent_post,
		'recent_prayers': recent_prayers,
		'recent_reflections': recent_reflections,
	})


def admin_login(request):
	# Always require pre-auth verification before showing the login form
	if request.method == 'GET':
		# If coming back from registration, show a single success message on the login page
		if request.GET.get('created') == '1':
			messages.success(request, 'Admin account created. Please log in.')
		if request.GET.get('verified') != '1':
			created_suffix = '&created=1' if request.GET.get('created') == '1' else ''
			return redirect(f"{reverse('admin_auth')}?next=admin_login{created_suffix}")

	if request.method == 'POST':
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		remember = request.POST.get('remember') == 'on'

		# Find user by email
		user = None
		if email:
			try:
				u = User.objects.get(email__iexact=email)
				user = authenticate(request, username=u.username, password=password)
			except User.DoesNotExist:
				user = None

		if user is not None and user.is_staff:
			login(request, user)
			# Remember me: set session expiry accordingly
			if remember:
				request.session.set_expiry(60 * 60 * 24 * 14)  # 14 days
			else:
				request.session.set_expiry(0)  # Browser-session only
			return redirect('admin_dashboard')

		if user is None:
			messages.error(request, 'Invalid email or password.')
		else:
			messages.error(request, 'You do not have admin access.')

	return render(request, 'pages/admin_login.html')


def admin_dashboard(request):
	# BYPASS: Allow access for anyone (for local dev/design)
	return render(request, 'pages/admin_dashboard.html')


def _require_staff(request):
	if not request.user.is_authenticated:
		return redirect('admin_login')
	if not request.user.is_staff:
		messages.error(request, 'Admin access required.')
		return redirect('home')
	return None


def manage_content(request):
	guard = _require_staff(request)
	if guard:
		return guard

	if request.method == 'POST':
		action = request.POST.get('action')
		if action == 'deliver':
			content = request.POST.get('content', '').strip()
			user_ids = request.POST.getlist('user_ids')
			if not content:
				messages.error(request, 'Content cannot be empty.')
			else:
				created = 0
				for uid in user_ids:
					try:
						u = User.objects.get(id=uid)
						Reflection.objects.create(user=u, text=content)
						created += 1
					except User.DoesNotExist:
						continue
				if created:
					messages.success(request, f'Delivered content to {created} user(s).')
				else:
					messages.info(request, 'No recipients selected; nothing delivered.')
			return redirect('manage_content')

	users = User.objects.all().order_by('username')
	recent_reflections = Reflection.objects.select_related('user').order_by('-created_at')[:10]
	return render(request, 'pages/manage_content.html', {
		'users': users,
		'recent_reflections': recent_reflections,
	})


def manage_feedback(request):
	# Bypass staff check for design preview
	feedbacks = Feedback.objects.select_related('user').order_by('-created_at')[:50]
	return render(request, 'pages/manage_feedback.html', {'feedbacks': feedbacks})


def manage_user(request):
	guard = _require_staff(request)
	if guard:
		return guard

	if request.method == 'POST':
		action = request.POST.get('action')
		user_id = request.POST.get('user_id')
		try:
			target = User.objects.get(id=user_id)
		except (User.DoesNotExist, ValueError, TypeError):
			target = None

		if action == 'toggle_role' and target:
			target.is_staff = not target.is_staff
			target.save()
			messages.success(request, f"Updated role for {target.username} to {'Admin' if target.is_staff else 'User'}.")
			return redirect('manage_user')
		elif action == 'delete_user' and target:
			username = target.username
			if target == request.user:
				messages.error(request, "You can't delete your own account while logged in.")
			else:
				target.delete()
				messages.success(request, f'Deleted account {username}.')
			return redirect('manage_user')

	admins = User.objects.filter(is_staff=True).order_by('username')
	users = User.objects.filter(is_staff=False).order_by('username')
	return render(request, 'pages/manage_user.html', {'admins': admins, 'users': users})


def manage_prayer(request):
	guard = _require_staff(request)
	if guard:
		return guard

	if request.method == 'POST':
		action = request.POST.get('action')
		if action == 'respond':
			req_id = request.POST.get('request_id')
			response = request.POST.get('response', '').strip()
			try:
				pr = PrayerRequest.objects.get(id=req_id)
				if not response:
					messages.error(request, 'Response cannot be empty.')
				else:
					pr.admin_response = response
					pr.status = 'responded'
					pr.responded_at = timezone.now()
					pr.save()
					messages.success(request, 'Response saved and request marked as responded.')
			except (PrayerRequest.DoesNotExist, ValueError, TypeError):
				messages.error(request, 'Prayer request not found.')
			return redirect('manage_prayer')

	requests_qs = PrayerRequest.objects.select_related('user').order_by('-created_at')
	pending = [r for r in requests_qs if not r.admin_response]
	return render(request, 'pages/manage_prayer.html', {'requests': pending})


def manage_prayer_history(request):
	guard = _require_staff(request)
	if guard:
		return guard
	responded = PrayerRequest.objects.select_related('user').exclude(admin_response='').order_by('-responded_at', '-created_at')
	return render(request, 'pages/manage_prayer_history.html', {'requests': responded})


def admin_register(request):
	# Always require pre-auth verification before showing the registration form
	if request.method == 'GET' and request.GET.get('verified') != '1':
		return redirect(f"{reverse('admin_auth')}?next=admin_register")

	# Public admin creation
	if request.method == 'POST':
		full_name = request.POST.get('full_name', '').strip()
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		mobile = request.POST.get('mobile', '').strip()  # optional, not stored on User
		password1 = request.POST.get('password1', '')
		password2 = request.POST.get('password2', '')

		# Basic field validations
		if not username or not email or not password1 or not password2:
			messages.error(request, 'Please fill in all required fields.')
			return render(request, 'pages/admin_register.html', {
				'prefill': {'full_name': full_name, 'username': username, 'email': email, 'mobile': mobile}
			})
		if password1 != password2:
			messages.error(request, 'Passwords do not match.')
			return render(request, 'pages/admin_register.html', {
				'prefill': {'full_name': full_name, 'username': username, 'email': email, 'mobile': mobile}
			})
		if User.objects.filter(username__iexact=username).exists():
			messages.error(request, 'This username is already taken.')
			return render(request, 'pages/admin_register.html', {
				'prefill': {'full_name': full_name, 'username': username, 'email': email, 'mobile': mobile}
			})
		if User.objects.filter(email__iexact=email).exists():
			messages.error(request, 'An account with this email already exists.')
			return render(request, 'pages/admin_register.html', {
				'prefill': {'full_name': full_name, 'username': username, 'email': email, 'mobile': mobile}
			})

		first_name = ''
		last_name = ''
		if full_name:
			parts = full_name.split()
			first_name = parts[0]
			last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

		# Create staff user
		user = User.objects.create_user(
			username=username,
			email=email,
			password=password1,
			first_name=first_name,
			last_name=last_name,
		)
		user.is_staff = True
		user.save()
		# Redirect to admin_auth with a created flag; after verification user will be sent to admin_login
		return redirect(f"{reverse('admin_auth')}?next=admin_login&created=1")

	return render(request, 'pages/admin_register.html')


def admin_auth(request):
	# Admin pre-authentication: require permanent code only
	if request.method == 'POST':
		code = request.POST.get('code', '').strip()
		next_name = request.POST.get('next') or 'admin_login'
		created_flag = request.POST.get('created')

		configured_code = getattr(settings, 'ADMIN_AUTH_CODE', '')

		if not configured_code:
			messages.error(request, 'Admin authentication is not configured. Please set ADMIN_AUTH_CODE.')
			return render(request, 'pages/admin_auth.html', {'next': next_name})

		if code == configured_code:
			# Avoid adding a success message here to prevent duplicates; carry created flag forward
			try:
				suffix = '&created=1' if created_flag == '1' else ''
				return redirect(f"{reverse(next_name)}?verified=1{suffix}")
			except Exception:
				return redirect('admin_login')
		else:
			messages.error(request, 'Invalid authentication code.')

	# GET
	next_name = request.GET.get('next') or 'admin_login'
	created_flag = request.GET.get('created')
	return render(request, 'pages/admin_auth.html', {'next': next_name, 'created': created_flag})


def journal(request):
	if not request.user.is_authenticated:
		# Provide dummy data for design preview
		class DummyUser:
			username = 'demo_user'
			def get_full_name(self): return 'Demo User'
		request.user = DummyUser()
		form = JournalEntryForm()
		entries = []
		grouped_entries = []
	else:
		if request.method == 'POST':
			form = JournalEntryForm(request.POST)
			if form.is_valid():
				je = form.save(commit=False)
				je.user = request.user
				je.save()
				messages.success(request, 'Journal entry saved.')
				return redirect('journal')
		else:
			form = JournalEntryForm()
		entries = JournalEntry.objects.filter(user=request.user).order_by('-date', '-created_at')
		from itertools import groupby
		from operator import attrgetter
		grouped_entries = []
		for date, entries_on_date in groupby(entries, key=attrgetter('date')):
			grouped_entries.append({
				'date': date,
				'entries': list(entries_on_date)
			})
	return render(request, 'pages/journal.html', {'form': form, 'entries': entries, 'grouped_entries': grouped_entries})


def edit_profile(request):
	if not request.user.is_authenticated:
		return redirect('login')

	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
		user_profile = UserProfile(user=request.user)

	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=user_profile)
		if form.is_valid():
			# Update User model fields
			if form.cleaned_data.get('full_name'):
				full_name = form.cleaned_data['full_name'].strip()
				parts = full_name.split()
				request.user.first_name = parts[0]
				request.user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''

			if form.cleaned_data.get('username'):
				new_username = form.cleaned_data['username'].strip()
				if new_username != request.user.username:
					if User.objects.filter(username__iexact=new_username).exists():
						messages.error(request, 'This username is already taken.')
						return render(request, 'pages/edit_profile.html', {'form': form})
					request.user.username = new_username

			# Handle password change if provided
			password1 = form.cleaned_data.get('password1')
			password2 = form.cleaned_data.get('password2')
			if password1 and password2:
				if password1 != password2:
					messages.error(request, 'Passwords do not match.')
					return render(request, 'pages/edit_profile.html', {'form': form})
				request.user.set_password(password1)
				# We'll need to re-login the user after password change
				updated_user = authenticate(username=request.user.username, password=password1)
				login(request, updated_user)

			request.user.save()

			# Save the profile with the image
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()

			messages.success(request, 'Profile updated successfully.')
			return redirect('profile')
	else:
		# Pre-fill the form with current user data
		initial_data = {
			'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
			'username': request.user.username,
		}
		form = ProfileForm(instance=user_profile, initial=initial_data)

	return render(request, 'pages/edit_profile.html', {'form': form})


def user_prayer_request(request):
	if not request.user.is_authenticated:
		# Provide dummy data for design preview
		class DummyUser:
			username = 'demo_user'
			def get_full_name(self): return 'Demo User'
		request.user = DummyUser()
		form = PrayerRequestForm()
		requests_qs = []
	else:
		if request.method == 'POST':
			form = PrayerRequestForm(request.POST)
			if form.is_valid():
				# Prevent accidental duplicate submissions within a short time window
				text = form.cleaned_data.get('text', '').strip()
				recent_window = now() - timedelta(minutes=5)
				dup_exists = PrayerRequest.objects.filter(user=request.user, text__iexact=text, created_at__gte=recent_window).exists()
				if dup_exists:
					messages.info(request, 'We detected a similar recent prayer request and avoided creating a duplicate.')
				else:
					pr = form.save(commit=False)
					pr.user = request.user
					pr.save()
					messages.success(request, 'Prayer request submitted.')
				return redirect('user_prayer_request')
		else:
			form = PrayerRequestForm()
		requests_qs = PrayerRequest.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'pages/user_prayer_request.html', {'form': form, 'requests': requests_qs})


def user_reflection(request):
	if request.method == 'POST':
		form = ReflectionForm(request.POST)
		if form.is_valid():
			r = form.save(commit=False)
			r.user = request.user
			r.save()
			messages.success(request, 'Reflection submitted.')
			return redirect('user_reflection')
	else:
		form = ReflectionForm()
	# Allow unauthenticated preview with mock data
	if request.user.is_authenticated:
		reflections = Reflection.objects.filter(user=request.user).order_by('-created_at')
	else:
		reflections = [type('Mock', (), {'text': 'This is a sample reflection for preview.', 'created_at': None})()]
	return render(request, 'pages/user_reflection.html', {'form': form, 'reflections': reflections})


def user_feedback(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():
			fb = form.save(commit=False)
			fb.user = request.user if request.user.is_authenticated else None
			fb.save()
			messages.success(request, 'Feedback saved. Thank you!')
			return redirect('user_feedback')
	else:
		form = FeedbackForm()
	if request.user.is_authenticated:
		recent_feedback = Feedback.objects.filter(user=request.user).order_by('-created_at')[:5]
	else:
		# Provide mock feedback for design preview
		from types import SimpleNamespace
		recent_feedback = [
			SimpleNamespace(created_at='2025-09-29', text='Great app! Very helpful for my daily devotion.'),
			SimpleNamespace(created_at='2025-09-28', text='Found a bug in the journal section.'),
		]
	return render(request, 'pages/user_feedback.html', {'form': form, 'recent_feedback': recent_feedback})


def logout_view(request):
	# Clear any admin pre-auth flag as well
	try:
		request.session['admin_pre_auth_ok'] = False
	except Exception:
		pass
	logout(request)
	return redirect('home')

# Create your views here.

def healthz(request):
	"""Lightweight health endpoint to verify DB connectivity on Render.
	Returns 200 with status and engine on success, 500 with error summary on failure.
	"""
	from django.db import connection
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT 1;")
			row = cursor.fetchone()
		status = 'ok' if row and row[0] == 1 else 'db-fail'
		return HttpResponse(f"status={status}\nengine={connection.vendor}", content_type="text/plain")
	except Exception as e:
		msg = str(e)
		return HttpResponse(f"status=db-error\nerror={msg}", content_type="text/plain", status=500)
