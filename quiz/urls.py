from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import (
    index,
    register,
    loginView,
    logout_view,
    HomeUser,
    action,
    panel,
    contact,
)

urlpatterns = [
    path('', index, name='index'),
    path('HomeUser/', HomeUser, name='HomeUser'),
    path('login/', loginView, name='login'),
    path('logout_view/', logout_view, name='logout_view'),
    path('register/', register, name='register'),
    path('panel/', panel, name='panel'),
    path('action/', action, name='action'),
    path('contact/', contact, name='contact'),
]

urlpatterns += staticfiles_urlpatterns()
