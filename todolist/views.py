from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from todolist.models import Todolist
from todolist.serializers import TodoItemSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

# Create your views here.
class TodoItemView(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = []
    
    def get_object(self, pk):
        try:
            return Todolist.objects.get(pk=pk)
        except Todolist.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        todos = Todolist.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TodoItemSerializer(data=request.data)
        serializer.author = request.user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        todo = self.get_object(pk)
        serializer = TodoItemSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })