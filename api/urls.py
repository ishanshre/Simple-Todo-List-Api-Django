from django.urls import path
from . import views

app_name='api'
urlpatterns = [
    path('',views.TodoListView.as_view()),
    path('create/',views.TodoListCreateView.as_view()),
    path('<int:pk>/', views.TodoUpdateDeleteView.as_view()),
    path('<int:pk>/complete/', views.TodoToogleCompleteView.as_view()),
    path('signup/', views.signup),
    path('login/', views.login),
]