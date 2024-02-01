import secrets
import string
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from app.models import OneTimeCode, Author


def register_first(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if username and email and password:
                user = User.objects.create_user(username=username, email=email, password=password)
                code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                onetime = OneTimeCode.objects.create(code=code, user=user)

                subject = 'Welcome!'
                text = f'{user.username}, you have successfully registered! Please this code {onetime.code} in website in order to complete the registration '
                html = (
                    f'<b>{user.username}</b>, you have successfully registered!'
                    f'<i> Please this code {onetime.code} in website in order to complete the registration </i>!'
                )
                msg = EmailMultiAlternatives(
                    subject=subject, body=text, from_email=None, to=[email]
                )
                msg.attach_alternative(html, "text/html")
                msg.send()

                return redirect('register2')

        except Exception as e:
            print(f"Error during user registration: {e}")

    return render(request, 'registration/registration.html')


def register_second(request):
    username = request.POST.get('username')
    code = request.POST.get('code')
    if OneTimeCode.objects.filter(code=code, user__username=username).exists():
        user = User.objects.get(username=username)
        Author.objects.create(user=user)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        login(request, user)
        return redirect('posts_list')

    return render(request, 'registration/confirmation.html')


def log_out(request):
    logout(request)

    return redirect('/posts')


def log_in(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts_list')

    return render(request, 'registration/login.html')
