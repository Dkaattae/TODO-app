from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from django.utils import timezone
from .forms import TodoForm

def todo_list(request):
    todos = Todo.objects.all()
    return render(request, 'todo/list.html', {'todos': todos})

def todo_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_completed = True
    todo.save()
    return redirect('todo_list')

def todo_remove(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list')

def todo_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/form.html', {'form': form})