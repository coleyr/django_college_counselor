from django import forms
from apps.home.models import ToDoList, ToDoItem
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit


class TodoListForm(forms.ModelForm):

    class Meta:
        model = ToDoList
        fields="__all__"

class TodoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields="__all__"
        
