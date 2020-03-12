from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


def get_redirect_to_home(request):
    return redirect("home_page_url")


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


def page_403(request, exception):
    # to check it add in view function
    # raise PermissionDenied
    response = render(request, "403.html", context={'error_status_code': 403})
    response.status_code = 403
    return response


def page_404(request, exception):
    response = render(request, "404.html", context={'error_status_code': 404})
    response.status_code = 404
    return response


def page_500(request):
    response = render(request, "500.html", context={'error_status_code': 500})
    response.status_code = 500
    return response