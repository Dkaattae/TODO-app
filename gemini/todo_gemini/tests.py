from django.test import TestCase
from django.urls import reverse
from .models import Todo
from django.utils import timezone
from datetime import timedelta

class TodoGeminiTests(TestCase):
    
    def test_create_todo_works_and_shows(self):
        """Test that creating a todo works and it appears on the list"""
        # Create a todo via POST
        data = {
            'title': 'Test Gemini Todo',
            'description': 'This is a test todo from Gemini',
            'due_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        }
        response = self.client.post(reverse('todo_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect to list
        
        # Check it was created in database
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'Test Gemini Todo')
        self.assertEqual(todo.description, 'This is a test todo from Gemini')
        
        # Check it shows on the list page
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Test Gemini Todo')
        self.assertContains(response, 'This is a test todo from Gemini')
    
    def test_remove_todo_works_and_not_showing(self):
        """Test that removing a todo works and it no longer appears"""
        # Create a todo
        todo = Todo.objects.create(
            title='Todo to Remove',
            description='This will be removed',
            due_date=timezone.now() + timedelta(days=1)
        )
        
        # Check it exists
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Todo to Remove')
        
        # Remove it
        response = self.client.post(reverse('todo_remove', args=[todo.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Check it's gone from database
        self.assertEqual(Todo.objects.count(), 0)
        
        # Check it doesn't show on the list
        response = self.client.get(reverse('todo_list'))
        self.assertNotContains(response, 'Todo to Remove')
    
    def test_complete_button_works_and_marked_completed(self):
        """Test that the complete button works and marks todo as completed"""
        # Create an incomplete todo
        todo = Todo.objects.create(
            title='Todo to Complete',
            description='This will be completed',
            due_date=timezone.now() + timedelta(days=5),  # More than 48 hours away
            is_completed=False
        )
        
        # Check it's initially incomplete
        todo.refresh_from_db()
        self.assertFalse(todo.is_completed)
        self.assertEqual(todo.status, 'Pending')
        
        # Complete it
        response = self.client.post(reverse('todo_complete', args=[todo.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Check it's now completed
        todo.refresh_from_db()
        self.assertTrue(todo.is_completed)
        self.assertEqual(todo.status, 'Completed')
        
        # Check the list shows it as completed
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Todo to Complete')
        self.assertContains(response, 'Completed')  # Status badge
    
    def test_todo_status_logic(self):
        """Test the status property logic"""
        now = timezone.now()
        
        # Test completed
        completed_todo = Todo.objects.create(
            title='Completed',
            due_date=now + timedelta(days=1),
            is_completed=True
        )
        self.assertEqual(completed_todo.status, 'Completed')
        
        # Test due soon (within 48 hours)
        due_soon_todo = Todo.objects.create(
            title='Due Soon',
            due_date=now + timedelta(hours=24),
            is_completed=False
        )
        self.assertEqual(due_soon_todo.status, 'Due Soon')
        
        # Test overdue
        overdue_todo = Todo.objects.create(
            title='Overdue',
            due_date=now - timedelta(hours=1),
            is_completed=False
        )
        self.assertEqual(overdue_todo.status, 'Overdue')
        
        # Test pending (more than 48 hours away)
        pending_todo = Todo.objects.create(
            title='Pending',
            due_date=now + timedelta(days=5),
            is_completed=False
        )
        self.assertEqual(pending_todo.status, 'Pending')
