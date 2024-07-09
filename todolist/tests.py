from unittest.mock import MagicMock
from django.http import Http404
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from todolist.models import Todolist
from todolist.views import TodoItemView

# Create your tests here.
class TestTodolist(TestCase):
    
    def setUp(self):
        #created new testing User
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        #Creation of a new token for a test user
        self.token, created = Token.objects.get_or_create(user=self.user)
        
         # Initialise the APIClient and set the token in the header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create some test data for todo lists
        self.todo1 = Todolist.objects.create(
            title='Todo1',
            description='Description for Todo1',
            author=self.user,
            priority='MEDIUM',
            dateline=None,
            state=None)
        self.todo2 = Todolist.objects.create(
            title='Todo2',
            description='Description for Todo2',
            author=self.user,
            priority='HIGH',
            dateline=None,
            state='InProgress')
        
    def test_logIn(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        
    def test_createUser(self):
        url = reverse('register')
        response = self.client.post(url, {'username':'testuser1', 'email':'test@email.com', 'password':'testpassword'})           
        self.assertEqual(response.status_code, 201)
    
    def test_todolist(self):
        url = reverse('todo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_create_todo(self):
        self.client.login(username='testuser', password='testpassword')
        data = {'title': 'Test Todo', 'description':'Test description', 'author':'1'}
        response = self.client.post(reverse('todo-list'), data, format='json')      
        self.assertEqual(response.status_code, 201)
        
    #def test_patch_todo(self):
    #    self.client.login(username='testuser', password='testpassword')
    #    data = {'title': 'Test Todo1', 'description':'Test description', 'author':'1'}
    #    response = self.client.patch(f'todos/{self.todo1}/', data, format='json')
    #    self.assertEqual(response.status_code, 200)
    
    def test_patch_todo(self):
        data = {'title': 'Test Todo1', 'description': 'Test description'}
        response = self.client.patch(reverse('todo-detail', args=[self.todo1.id]), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Test Todo1')
        self.assertEqual(self.todo1.description, 'Test description')
        
    def test_delete_todo(self):
        response = self.client.delete(reverse('todo-detail', args=[self.todo1.id]))
        self.assertEqual(response.status_code, 204)
        
        with self.assertRaises(Todolist.DoesNotExist):
            Todolist.objects.get(id=self.todo1.id)
        
        
        