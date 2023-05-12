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
    results
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
    path('results/', results, name='results'),
]

urlpatterns += staticfiles_urlpatterns()
