from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm
from datetime import date, timedelta

def todo_list(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    
    todos = Todo.objects.all()
    today = date.today()
    for todo in todos:
        if todo.due_date and not todo.is_completed:
            days_left = (todo.due_date - today).days
            if days_left <= 3 and days_left >= 0:
                todo.status = 'due_soon'
            elif days_left < 0:
                todo.status = 'overdue'
            else:
                todo.status = 'pending'
        else:
            todo.status = 'completed' if todo.is_completed else 'pending'
    
    return render(request, 'todo/todo_list.html', {'todos': todos, 'form': form})

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect('todo_list')

def toggle_complete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('todo_list')
