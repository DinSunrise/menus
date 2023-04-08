from django.urls import path
from menus.views import index

urlpatterns = [
    path('', index, name='index'),
]
