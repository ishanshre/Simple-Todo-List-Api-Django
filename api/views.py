from django.shortcuts import render
from .serializer import TodoSerializer
from rest_framework import generics
from todo.models import Todo
# Create your views here.

class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)