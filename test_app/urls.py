from django.urls import path
from . import views


urlpatterns = [
    path('', views.test_view, name='test-view'),
]
