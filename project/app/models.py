from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=255,)

    def __str__(self):
        return self.category_name


class Post(models.Model):

    post_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=False, max_length=255)
    content = RichTextField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved = True
        self.save()


class OneTimeCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

