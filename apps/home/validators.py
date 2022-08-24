from functools import wraps
from apps.home.models import Counselor, Parent, Student, User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse



def get_user_object(object, user):
    try:
        return object.objects.get(user=user)
    except object.DoesNotExist:
        return None
    
def validate_student_view(request, student):
    # IF student viewing themselves
    if request.user == student:
        return True
    counselor = get_user_object(Counselor, request.user)
    if counselor:
        return True
    parent = get_user_object(Parent, request.user)
    if parent:
        return parent.student.filter(user=student).exists()

def get_student_from_name(name: str, request):
    student, error = None, None
    try:
        first_name, last_name = name.split()
        student_user = User.objects.get(first_name=first_name, last_name=last_name)
        student = Student.objects.get(user=student_user)
    except User.DoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        error = HttpResponse(html_template.render({}, request))
    except Student.DoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        error = HttpResponse(html_template.render({}, request))
    return student, error

def user_can_view_student():
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            student, error = get_student_from_name(kwargs['name'], request)
            if error:
                return error
            if not validate_student_view(request, student):
                return HttpResponseRedirect(reverse('home'))

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

