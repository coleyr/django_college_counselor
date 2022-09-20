# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.utils.timezone import make_aware
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import Counselor, Student, Parent, ToDoItem, ToDoList, User
from apps.home.validators import user_can_view_student, get_user_from_id
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory
## import todo form and models
from apps.home.forms import TodoItemForm, TodoListForm
###############################################


def get_username(request):
    return request.user.username if request.user.is_authenticated else None

def get_students(request):
    if request.user.is_authenticated and request.user.role == 2:
        try:
            user = Counselor.objects.get(user=request.user)
            return Student.objects.filter(counselor=user)
        except Exception:
            return []
    if request.user.is_authenticated and request.user.role == 3:
        try:
            user = Parent.objects.get(user=request.user)
            return user.student.filter()
        except Exception:
            return []
    return []


def get_role_name(user):
    role_name = None
    for choice in User.ROLE_CHOICES:
        if choice[0] == user.role:
            role_name = choice[1]
    return role_name

def get_dashboard_data(request):
    data = {"user": request.user}
    data['role_name'] = get_role_name(request.user)
    user_types = {"STUDENT":Student, "COUNSELOR":Counselor, "PARENT":Parent}
    for user_type_name, user_class in user_types.items():
        try:
            subclass_user = user_class.objects.get(user=request.user)
            data[user_type_name] = subclass_user
        except Exception:
            data[user_type_name] = None
    data['todos'] = get_to_dos(request.user)
    return data

def get_to_dos(user):
    for todo in ToDoItem.objects.filter(assignee=user):
        yield todo

def get_todo_bound_forms(user):
    forms = [TodoItemForm(instance=todo) for todo in get_to_dos(user)]
    forms = [{"bound_form":TodoItemForm(instance=todo_list), "id":todo_list.id} for todo_list in get_to_dos(user)]
    return forms, TodoItemForm()

# def get_todo_list_bound_forms(user):
#     forms = [{"bound_form":TodoListForm(instance=todo_list), "id":todo_list.id} for todo_list in get_to_do_list(user)]
#     # for item in forms:
#     #     item.set_readonly()
#     forms.append({"bound_form":TodoListForm(), "id":"None"})
#     return forms

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['user'] = get_dashboard_data(request)
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request, *args, **kwargs):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        if load_template == 'tables.html':
            context['students'] = get_students(request)
        if load_template == 'index.html':
            context['user'] = get_dashboard_data(request)
        if load_template == 'todo_list.html':
            return redirect(to_do_list, request.user.id)
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print(e)
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
@user_can_view_student()
def student_page(request, id:str):
    #Get The name of the user... could use user_id...
    student, error = get_user_from_id(id, request)
    forms, create_form = get_todo_bound_forms(student.user)
    role_name = get_role_name(student.user)
    if request.method == "POST":
        form = TodoItemForm(request.POST)
        if form.is_valid():
            list_obj = form.save()
            list_obj.assignee = student.user
            list_obj.save()
    if error:
        return error
    context = {'student':student, 'forms':forms, 'role_name':role_name}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        html_template = loader.get_template('home/student.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print(e)
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
#ok
@login_required(login_url="/login/")
@user_can_view_student()
def to_do_list(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = TodoItemForm(request.POST)

        if form.is_valid():
            print("Form valid")
            list_obj = form.save()
            list_obj.assignee = user
            list_obj.save()

    forms, create_form = get_todo_bound_forms(user)
    page = {
                "id": id,
             "forms" : forms,
             "create_form": create_form,
             "title" : "TODO LIST",
           }
    return render(request, 'home/todo_list.html', page)

@login_required(login_url="/login/")
@user_can_view_student()
def delete_todo_item(request, id, todolist_id):
    if todolist_id in {"None", None}:
       return redirect(to_do_list, id)
    user = User.objects.get(id=id)
    todoitem_del_list = ToDoItem.objects.filter(assignee=user, id=todolist_id)
    for todoitem in todoitem_del_list:
        todoitem.delete()
    return redirect(to_do_list, id)