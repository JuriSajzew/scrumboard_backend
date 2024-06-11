from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response

from todolist.models import Todolist
from todolist.serializers import TodoItemSerializer

# Create your views here.
class TodoItemView(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        todos = Todolist.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
    