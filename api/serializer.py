from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated  = serializers.ReadOnlyField()
    completed  = serializers.ReadOnlyField()
    class Meta:
        model = Todo
        fields = ['id','title','body','created','updated','completed']