from rest_framework import serializers
from todolist.models import Todolist

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = '__all__'
        
from django.contrib.auth import get_user_model        
class UserItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Verwenden Sie get_user_model(), um das aktuelle Benutzermodell zu erhalten
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user