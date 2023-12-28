from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


class RegisterView(View):
    # Встановлюємо шаблон для відображення форми реєстрації
    template_name = "users/register.html"
    # Встановлюємо клас форми реєстрації
    form_class = RegisterForm

    # Перевантажуємо метод dispatch для перевірки автентифікації користувача
    def dispatch(self, request, *args: Any, **kwargs: Any):
        # Якщо користувач вже автентифікований, перенаправляємо його на головну сторінку
        if request.user.is_authenticated:
            return redirect("quotes:root")
        # Якщо користувач не автентифікований, викликаємо метод батьківського класу
        return super().dispatch(request, *args, **kwargs)

    # Обробляємо GET-запит
    def get(self, request):
        # Відображаємо форму реєстрації
        return render(request, self.template_name, {"form": self.form_class})

    # Обробляємо POST-запит
    def post(self, request):
        # Створюємо екземпляр форми реєстрації з даними з POST-запиту
        form = self.form_class(request.POST)
        # Якщо форма валідна, зберігаємо її, показуємо повідомлення про успішне створення аккаунту та перенаправляємо
        # користувача на сторінку входу
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, message=f"Вітаємо {username}. Ваш аккаунт успішно створено.")
            return redirect(reverse_lazy("users:login"))
        # Якщо форма не валідна, відображаємо її з помилками
        return render(request, self.template_name, {"form": form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'