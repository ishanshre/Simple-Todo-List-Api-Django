from django.shortcuts import render
from .serializer import TodoSerializer, TodoToogleCompleteSerializer
from rest_framework import generics, permissions
from todo.models import Todo
# Create your views here.

class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')


class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user).order_by('-created')
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class TodoUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)


class TodoToogleCompleteView(generics.UpdateAPIView):
    serializer_class = TodoToogleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save()