from django.test import TestCase
from django.urls import reverse
from .models import Todo

class TodoAppTests(TestCase):
    
    def test_homepage_loads_correctly(self):
        """Test that the homepage loads with status 200"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Todo List')
    
    def test_todo_creation(self):
        """Test that a todo can be created via POST"""
        data = {
            'title': 'Test Todo',
            'description': 'This is a test todo',
            'due_date': '2026-01-20',
            'is_completed': False
        }
        response = self.client.post(reverse('todo_list'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'Test Todo')
        self.assertEqual(todo.description, 'This is a test todo')
        self.assertFalse(todo.is_completed)
    
    def test_todo_shows_on_homepage(self):
        """Test that created todos appear on the homepage"""
        todo = Todo.objects.create(
            title='Visible Todo',
            description='Should be visible',
            due_date='2026-01-25'
        )
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Visible Todo')
        self.assertContains(response, 'Should be visible')
    
    def test_todo_in_database(self):
        """Test that todos are properly saved to the database"""
        Todo.objects.create(
            title='DB Test',
            description='Testing database storage'
        )
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.get(title='DB Test')
        self.assertEqual(todo.description, 'Testing database storage')
        self.assertFalse(todo.is_completed)
    
    def test_todo_can_be_marked_completed(self):
        """Test that a todo can be marked as completed"""
        todo = Todo.objects.create(
            title='Complete Me',
            is_completed=False
        )
        response = self.client.post(reverse('toggle_complete', args=[todo.id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        todo.refresh_from_db()
        self.assertTrue(todo.is_completed)
    
    def test_todo_can_be_removed(self):
        """Test that a todo can be deleted"""
        todo = Todo.objects.create(title='Delete Me')
        self.assertEqual(Todo.objects.count(), 1)
        response = self.client.post(reverse('delete_todo', args=[todo.id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Todo.objects.count(), 0)
    
    def test_removed_todo_not_showing(self):
        """Test that deleted todos don't appear on the homepage"""
        todo = Todo.objects.create(title='Should Disappear')
        response = self.client.get(reverse('todo_list'))
        self.assertContains(response, 'Should Disappear')
        
        # Delete the todo
        self.client.post(reverse('delete_todo', args=[todo.id]))
        
        # Check it's not in the response anymore
        response = self.client.get(reverse('todo_list'))
        self.assertNotContains(response, 'Should Disappear')
    
    def test_toggle_complete_twice(self):
        """Test that toggling complete twice returns to incomplete"""
        todo = Todo.objects.create(title='Toggle Test', is_completed=False)
        # First toggle to complete
        self.client.post(reverse('toggle_complete', args=[todo.id]))
        todo.refresh_from_db()
        self.assertTrue(todo.is_completed)
        # Second toggle back to incomplete
        self.client.post(reverse('toggle_complete', args=[todo.id]))
        todo.refresh_from_db()
        self.assertFalse(todo.is_completed)
