# -*- encoding: utf-8 -*-


from django.contrib import admin
from apps.home.models import Student, Counselor, Parent, ToDoItem, ToDoList
# Register your models here.

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Counselor)
admin.site.register(ToDoItem)
admin.site.register(ToDoList)
