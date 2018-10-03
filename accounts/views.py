from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from AssetDatabase.models import Asset
from .forms import LoginForm


# Create your views here.
def profile(request, username):
    user = User.objects.get(username=username)
    assets = Asset.objects.filter(user=user)
    return render(request, 'accounts/profile.html', {'name': username, 'assets': assets})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
