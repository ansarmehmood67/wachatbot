from django.db import models

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Message Sent'),
        ('replied', 'User Replied'),
        ('reminded', 'Reminder Sent'),
        ('completed', 'Onboarding Completed'),
        ('escalated', 'Escalated to Admin'),  # ✅ Added for live chat
    ]

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    last_updated = models.DateTimeField(auto_now=True)
    history = models.JSONField(default=list, blank=True, null=True)  # 🧠 Stores chat history

    def __str__(self):
        return f"{self.name} {self.surname} ({self.phone_number}) - {self.status}"
