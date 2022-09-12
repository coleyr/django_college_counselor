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

def get_user_objects(objects, user):
    for object in objects:
        try:
            return object.objects.get(user=user)
        except object.DoesNotExist:
            pass

def validate_student_view(request, user):
    # IF student viewing themselves
    if request.user == user.user:
        return True
    counselor = get_user_object(Counselor, request.user)
    if counselor:
        return True
    parent = get_user_object(Parent, request.user)
    if parent:
        return parent.student.filter(user=user).exists()


def get_user_from_id(id: str, request):
    user, error = None, None
    user_types = [Student, Counselor, Parent]
    try:
        user_id = User.objects.get(id=id)
        user = get_user_objects(user_types, user_id)
    except User.DoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        error = HttpResponse(html_template.render({}, request))
    if not user: 
        html_template = loader.get_template('home/page-404.html')
        error = HttpResponse(html_template.render({}, request))
    return user, error

def user_can_view_student():
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            print(kwargs)
            user, error = get_user_from_id(kwargs['id'], request)
            if error:
                return error
            if not validate_student_view(request, user):
                html_template = loader.get_template('home/page-403.html')
                return HttpResponse(html_template.render({}, request))
                

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

