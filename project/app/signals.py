from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment


@receiver(post_save, sender=Comment)
def comment_added(instance,  **kwargs):
    if kwargs.get('created'):
        post = instance.post
        author = post.author
        user = author.user
        email = user.email

        subject = f'New Comment under your Post'

        text_content = (
            f'A New Comment under your Post: {instance.content}\n'
        )
        html_content = (
            f'A New Comment under your Post: {instance.content}<br>'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Comment)
def comment_approval(instance,  **kwargs):
    if instance.approved:
        user = instance.user
        email = user.email

        subject = f'Your Comment Has Been Approved'

        text_content = (
            f'Your Comment Has Been Approved: {instance.content}\n'
        )
        html_content = (
            f'Your Comment Has Been Approved: {instance.content}<br>'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
