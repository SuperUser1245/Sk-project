from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Post, OneTimeCode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User


@shared_task
def weekly_newsletter():
    posts = Post.objects.filter(post_time__gte=datetime.now() - timedelta(days=7))
    users = User.objects.all()
    for user in users:
        user_email = user.email
        html_content = render_to_string(
            'scheduler_app.html',
            {
                'posts': posts,
            }
        )

        send_mail(
            subject='All new posts from last Monday!',
            message='',
            html_message=html_content,
            from_email='example@gmail.com',
            recipient_list=user_email,
        )

@shared_task
def cleanup_codes():
    expired_codes = OneTimeCode.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(minutes=3))
    expired_codes.delete()
