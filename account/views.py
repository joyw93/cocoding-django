from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('cocoding:post_list')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'account/signup.html', context)


def signin(request):
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('cocoding:post_list')
        else:
            context = {'login_error_msg':'이메일 또는 비밀번호를 확인하세요.'}
            return render(request, 'account/signin.html', context)
    else:
        return render(request, 'account/signin.html')


def signout(request):
    logout(request)
    return redirect('cocoding:post_list')