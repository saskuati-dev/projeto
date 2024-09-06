from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .forms import RepresentanteLoginForm, RepresentanteRegistroForm
import logging

def logout_view(request):
    logout(request)
    return redirect('home')

def registro_representante(request):
    if request.method == 'POST':
        form = RepresentanteRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            representante = form.save() 
            group = Group.objects.get(name='Representante Esportivo')

            representante.user.groups.add(group)
            
            return redirect('login')
    else:
        form = RepresentanteRegistroForm()
    
    return render(request, 'html/registro.html', {'form': form})


def login_representante(request):
  if request.method == 'POST':
    form = RepresentanteLoginForm(data=request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        if user.groups.filter(name='Administrador Esportivo').exists():
            return render(request, 'html/adm.html')
        elif user.groups.filter(name='Representante Esportivo').exists():
            return render(request, 'html/user.html')
      else:
        form.add_error(None, 'CPF ou senha inválidos.')
  else:
    form = RepresentanteLoginForm()
  return render(request, 'html/login.html', {'form': form})

def download_document(request):
    file_path = 'media/documento/REPRESENTANTE_ESPORTIVO.pdf'
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Termo de Compromisso.pdf')

logger = logging.getLogger(__name__)



def is_admin_esportivo(user):
    return user.groups.filter(name='Administrador Esportivo').exists()

def is_representante_esportivo(user):
    return user.groups.filter(name='Representante Esportivo').exists()

@login_required(login_url='login')
def user(request):
    if not is_representante_esportivo(request.user):
        logout(request) 
        return redirect('home')
    return render(request, 'html/user.html')

@login_required(login_url='login')
def adm(request):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    return render(request, 'html/adm.html')

def home(request):
    return render(request, 'html/home.html')

def editais(request):
    return render(request, 'html/editais.html')

def sobre(request):
    return render(request, 'html/sobre.html')

