from rest_framework import serializers

from todolist.models import Todolist

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = '__all__'