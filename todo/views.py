# Добавляем redirect для перенаправления
import todowoo.urls
from django.shortcuts import render, redirect, get_object_or_404
# Импортируем готовое решение django для создания форм и добавляем аунтификацию
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Импортируем модель пользователя, с которой мы будем работать в дальнейшем
from django.contrib.auth.models import User
# Импортируем ошибку, которую хотим обработать
from django.db import IntegrityError
# Импортирует профиль пользователя и функцию выхода и функцию аунтификации
from django.contrib.auth import login, logout, authenticate
# Импортируем созданную форму
from .forms import TodoForm
from .models import Todo

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        # Передаем через словарь импортированную форму
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        # Проверка правильности ввода пароля
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Создать новый объект пользователя
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # Сохранение объекта пользователя в БД
                user.save()
                login(request, user)
                return redirect('currenttodos')
            # При совпадении имен пользователей, с последующей ошибкой IntegrityError вывести страницу с предупреждением
            # о том, что такой пользователь уже существует
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Pleace choice a new username'})
        else:
            # Выдать ошибку
            # error - название ключа ошибки
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        # Передаем через словарь импортированную форму
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        # Проверка соответствия логина и пароля при входе пользователя
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error':'Bad data passed in. Try again'})

def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'form': UserCreationForm(), 'todos':todos})

def viewtodo(request, todo_pk):
    viewtodo = get_object_or_404(Todo, pk=todo_pk)
    return render(request, 'todo/viewtodo.html', {'viewtodo':viewtodo})