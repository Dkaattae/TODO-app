from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none transition',
                'placeholder': 'What needs to be done?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none transition',
                'placeholder': 'Add some details...',
                'rows': 3
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 outline-none transition',
                'type': 'datetime-local' # This triggers the native browser picker
            }),
        }