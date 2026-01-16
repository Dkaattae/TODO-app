from django.db import models
from django.utils import timezone
from datetime import timedelta

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        if self.is_completed:
            return "Completed"
        
        now = timezone.now()
        # Logic: If due date is in the future AND less than 48 hours away
        if now <= self.due_date <= now + timedelta(hours=48):
            return "Due Soon"
        elif self.due_date < now:
            return "Overdue"
        return "Pending"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']
