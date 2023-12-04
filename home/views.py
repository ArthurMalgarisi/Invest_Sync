from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuario.models import Usuario


# Create your views here.

def home(request):
    user = request.user.id
    return render(request, 'home.html')


def home_log(request):
    user = request.user.id
    usuario = Usuario.objects.get(id=user)
    return render(request, 'home.html', {'usuario': usuario})