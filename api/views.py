from django.shortcuts import render
from .serializer import TodoSerializer, TodoToogleCompleteSerializer
from rest_framework import generics, permissions
from todo.models import Todo
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate
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


@csrf_exempt
def signup(request):
    User = get_user_model()
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username = data['username'],
                password = data['password'],
            )
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)

        except IntegrityError:
            return JsonResponse({'error':'username already taken, user another one'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)#convert json data to python dict
        user = authenticate(
            request,
            username=data['username'],
            password = data['password']
        )#save auth creditancials 
        if user is None:
            return JsonResponse({'error':'Wrong User name or password'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)#if token is not created
            return JsonResponse({'token':str(token)}, status=200)

