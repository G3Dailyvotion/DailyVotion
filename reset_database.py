#!/usr/bin/env python
"""
Reset Database Script for DailyVotion
This script will clear all PrayerRequest, JournalEntry, Reflection, and Feedback
records while preserving User accounts and profiles.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyvotion_django.settings")
django.setup()

from pages.models import JournalEntry, PrayerRequest, Reflection, Feedback
from django.contrib.auth.models import User
from django.db import transaction


def reset_content_data():
    """Delete all content data while preserving user accounts and profiles."""

    with transaction.atomic():
        # Get record counts before deletion
        journal_count = JournalEntry.objects.count()
        prayer_count = PrayerRequest.objects.count()
        reflection_count = Reflection.objects.count()
        feedback_count = Feedback.objects.count()
        user_count = User.objects.count()

        # Delete all content
        JournalEntry.objects.all().delete()
        PrayerRequest.objects.all().delete()
        Reflection.objects.all().delete()
        Feedback.objects.all().delete()

        # Print results
        print("===== DATABASE RESET SUMMARY =====")
        print(f"Users preserved: {User.objects.count()} (was {user_count})")
        print(f"Deleted journal entries: {journal_count}")
        print(f"Deleted prayer requests: {prayer_count}")
        print(f"Deleted reflections: {reflection_count}")
        print(f"Deleted feedback items: {feedback_count}")
        print("=================================")

        total_deleted = journal_count + prayer_count + reflection_count + feedback_count
        print(f"Total records deleted: {total_deleted}")
        print("User accounts and profiles have been preserved.")


if __name__ == "__main__":
    confirm = input("This will delete ALL journal entries, prayer requests, reflections, and feedback.\n"
                   "User accounts will be preserved. Type 'yes' to confirm: ")

    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        sys.exit(0)

    reset_content_data()
    print("Database reset completed successfully!")