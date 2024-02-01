from django.urls import path
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete, author_posts, add_comment_view, approve_comment, delete_comment)

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('<int:id>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:id>/edit/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('myposts/', author_posts, name='my_posts'),
    path('add_comment/<int:post_id>/', add_comment_view, name='add_comment'),
    path('approve_comment/<int:comment_id>/', approve_comment, name='approve_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

]
