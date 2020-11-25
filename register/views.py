from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views import View
from django.views.generic import CreateView, FormView, RedirectView, UpdateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from .models import User
from .forms import RegisterForm, LoginForm, SendEmailForm, PasswordResetCustomUserForm, SetPasswordCustomUserForm
from datetime import datetime, date


class PasswordResetCustomUser(FormView):
    # Used to customize the passowrd reset form

    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetCustomUserForm
    template_name = "register/password/password_reset.html"


class PasswordResetCustomUserConfirm(FormMixin, DetailView):

    success_url = reverse_lazy('password_reset_complete')
    template_name = 'register/password/password_reset_confirm.html'
    form_class = SetPasswordCustomUserForm
    model = User

    def get_object(self):
        id = urlsafe_base64_decode(self.kwargs['uidb64'])
        user = get_object_or_404(User, id=id)
        return user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        request = self.request
        answer = form.cleaned_data.get("answer").lower()
        password = form.cleaned_data.get("new_password1")
        u = self.get_object()
        if answer == u.security_answer and not check_password(password, u.password):
            u.password_expiration = 0
            u.set_password(password)
            u.save()
            return super(PasswordResetCustomUserConfirm, self).form_valid(form)
        else:
            messages.error(request, "Password was not reset!")
            return super(PasswordResetCustomUserConfirm, self).form_invalid(form)


class SignUpView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'register/signup.html'


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'register/login.html'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        u = User.objects.filter(email=email).get()

        if not u.active:
            print("Deactive end date")
            now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            now_truncated = date(now.year, now.month, now.day)
            if u.deactive_time_end == now_truncated:
                print("Changed active user")
                u.active = True
                u.save()

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            u.password_expiration = abs(
                datetime.today().day - u.date_joined.day)
            u.save()
            if u.password_expiration != 3:
                messages.success(request, "Your password will expire in {} days".format(
                    abs(u.password_expiration - 3)))
                messages.success(
                    request, "You have successfully Logged In")
        else:
            if u.active:
                if request.session.get('count', 0) == 0:
                    request.session['count'] = 1
                    messages.error(
                        request, "Your account will be suspended after {} more attempts.".format(abs(3 - request.session['count'])))
                else:
                    request.session['count'] += 1
                    messages.error(
                        request, "Your account will be suspended after {} more attempts.".format(abs(3 - request.session['count'])))

                if request.session['count'] == 3:
                    request.session['count'] = 1
                    u.active = False
                    u.save()
                    messages.error(
                        request, "Your account has been suspended for 24 hours.")
            else:
                messages.error(
                    request, "This account is suspended, Contact your administrator for more information.")

        return super(LoginView, self).form_invalid(form)


class LogoutView(RedirectView):

    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            auth_logout(request)
            messages.success(request, "User Successfully Logged out")
            return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileView(ListView, FormView):

    model = User
    paginate_by = 25
    template_name = "register/userprofiles.html"

    form_class = SendEmailForm
    success_url = reverse_lazy('userprofiles')

    def form_valid(self, form):

        request = self.request
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        try:
            send_mail(
                subject,
                message,
                'movethewaters@gmail.com',
                [to_email],
                fail_silently=False,
            )
        except BadHeaderError:
            messages.error(request, "Email was not sent.")
            return super().form_invalid(form)

        messages.success(request, "Email was successfully sent.")
        return super().form_valid(form)


class UserProfileUpdateView(UpdateView):

    model = User
    fields = ['email', 'last_name', 'user_type', 'active',
              'address', 'city', 'zip_code', 'state', 'deactive_time_start',
              'deactive_time_end']
    success_url = reverse_lazy('userprofiles')
    template_name = "register/updateuser.html"

    def form_valid(self, form):

        request = self.request
        email = form.cleaned_data.get("email")
        active = form.cleaned_data.get("active")
        deactive_date = form.cleaned_data.get("deactive_time_start")
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        now_truncated = date(now.year, now.month, now.day)
        u = User.objects.filter(email=email).get()

        if request.user.is_authenticated:

            if deactive_date == now_truncated:
                u.active = False
                u.save()
                messages.success(request, "User profile has been updated.")
                return super().form_valid(form)
            else:

                messages.success(request, "User profile has been updated.")
                return super().form_valid(form)

        messages.error(request, "Error user profile could not be updated.")
        return super().form_invalid(form)
