from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.http import HttpResponseForbidden


@login_required(login_url="/login/")
def add_comment_view(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        comment_content = request.POST.get('comment_content')

        if comment_content:
            Comment.objects.create(post=post, user=request.user, content=comment_content)

    return redirect('posts_list')


def approve_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.approve_comment()
    return redirect('my_posts')


def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('my_posts')


class PostList(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


@login_required(login_url="/login/")
def author_posts(request):
    user = User.objects.get(id=request.user.id)
    author = Author.objects.get(user_id=user)
    author_posts = Post.objects.filter(author=author)
    return render(request, 'user_post.html', {'author_posts': author_posts})


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('app.add_post',)
    form_class = PostForm
    model = Post
    success_url = '/posts/'
    template_name = 'create.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_post',)
    form_class = PostForm
    model = Post
    success_url = '/posts/'
    template_name = 'edit.html'
    pk_url_kwarg = 'id'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('app.delete_post',)
    model = Post
    template_name = 'delete.html'
    success_url = '/posts/'


