from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegisterForm()
        if request.method == 'POST' :
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                return redirect('account_login')

        context = {'form': form}
        return render(request, 'registration/signup.html', context)


def loginPage(request, next=None):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            next_url = request.GET.get('next')
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
            else:
                context = {'message': 'Username OR password is incorrect'}

        return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')