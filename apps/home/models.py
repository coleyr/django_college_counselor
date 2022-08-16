# -*- encoding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.urls import reverse
GRADE_CHOICES = (
    ('freshmen','FRESHMEN'),
    ('sophmore', 'SOPHMORE'),
    ('junior','JUNIOR'),
    ('senior','SENIOR'),
    ('grad','GRAD'),
)

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.EmailField()
    class Meta:
        abstract = True

class Counselor(Person):
    img = models.ImageField(blank=True)
    staff = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Student(Person):
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='freshmen')
    img = models.ImageField(blank=True)
    counselor = models.ForeignKey(Counselor, on_delete=models.DO_NOTHING)
    constraints = [
        models.UniqueConstraint(fields=['first_name', 'last_name', 'email'], name='student_name_unique_together_constraint')
    ]
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class Parent(Person):
    img = models.ImageField(blank=True)
    student = models.ManyToManyField(Student)
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return f"{self.student} - {self.title}"

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]