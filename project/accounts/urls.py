from django.urls import path, include
from .views import register_first, log_out, log_in, register_second


urlpatterns = [
    path('register/', register_first, name='register'),
    path('register2/', register_second, name='register2'),
    path('logout/', log_out, name='logout'),
    path('login/', log_in, name='login'),

]
