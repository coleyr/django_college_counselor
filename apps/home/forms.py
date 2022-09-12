from django import forms
from apps.home.models import ToDoList, ToDoItem
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit


class TodoListForm(forms.ModelForm):
    
    
    def set_readonly(self, field='assignee'):              
        self.fields[field].required = False
        self.fields[field].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = ToDoList
        fields="__all__"
        exclude = ('assignee',)


class TodoItemForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    class Meta:
        model = ToDoItem
        fields ="__all__"

        
