from django.urls import path

from core.homepage.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
