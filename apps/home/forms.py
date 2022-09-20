from pickletools import StackObject
from django import forms
from apps.home.models import ToDoList, ToDoItem


from apps.home.models import STATUS_CHOICES
class TodoListForm(forms.ModelForm):
    
    class Meta:
        model = ToDoList
        fields="__all__"



class TodoItemForm(forms.ModelForm):    
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'to_do_form'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'to_do_form'}))
    due_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type":"date"}))
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = ToDoItem
        exclude = ('assignee', 'todo_list')

        
