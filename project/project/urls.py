from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('app.urls')),
    path('', include('accounts.urls')),

]
