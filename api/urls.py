from django.urls import path
from . import views

app_name='api'
urlpatterns = [
    path('',views.TodoListView.as_view()),
    path('create/',views.TodoListCreateView.as_view()),
]