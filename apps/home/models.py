# -*- encoding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

GRADE_CHOICES = (
    ('freshman','FRESHMAN'),
    ('sophmore', 'SOPHMORE'),
    ('junior','JUNIOR'),
    ('senior','SENIOR'),
    ('grad','GRAD'),
)

STATUS_CHOICES =(
    ('Not Being Worked on','NOT BEING WORKED ON'),
    ('In Progress', 'IN PROGRESS'),
    ('Awaiting Feedback','AWAITING FEEDBACK'),
    ('Complete','COMPLETE'),
    ('stuck','STUCK'),
)

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class User(AbstractUser):
    STUDENT = 1
    COUNSELOR = 2
    PARENT = 3
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (COUNSELOR, 'Counselor'),
        (PARENT, 'Parent')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.username}"
    def __repr__(self) -> str:
        return self.__str__()
# Create your models here.
class Person(models.Model):
    img = models.ImageField(blank=True, upload_to='img', default=f'/img/student-icon.png')
    @property
    def get_photo_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        else:
            return "/media/img/student-icon.jpg"
        
    def __str__(self) -> str:
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"{self.user.username}"
    def __repr__(self) -> str:
        return self.__str__()
    class Meta:
        abstract = True

class Counselor(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Student(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='freshman')
    counselor = models.ForeignKey(Counselor, on_delete=models.DO_NOTHING, null=True, blank=True)
    constraints = [
        models.UniqueConstraint(fields=['user'], name='student_name_unique_together_constraint')
    ]

    
class Parent(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student = models.ManyToManyField(Student, blank=True)
    @property
    def student_names(self):
        student_names = " ".join(f"{student.user.first_name}, {student.user.last_name}" for student in self.student.all()) if self.student.all() else None
        return student_names

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return f"{self.title}"

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Being Worked on')
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]