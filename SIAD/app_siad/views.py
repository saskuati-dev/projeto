from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RepresentanteLoginForm, RepresentanteRegistroForm
import logging
from django.http import FileResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RepresentanteRegistroForm, RepresentanteLoginForm

def logout_view(request):
    logout(request)
    return redirect('home')
def registro_representante(request):
  if request.method == 'POST':
    form = RepresentanteRegistroForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return redirect('login')  # Redireciona para a página de login após o registro
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
        return redirect('home')  # Redireciona para a página inicial após o login
      else:
        form.add_error(None, 'CPF ou senha inválidos.')
  else:
    form = RepresentanteLoginForm()
  return render(request, 'html/login.html', {'form': form})

def download_document(request):
    file_path = 'media/documento/REPRESENTANTE_ESPORTIVO.pdf'
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Termo de Compromisso.pdf')

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'html/home.html')

def editais(request):
    return render(request, 'html/editais.html')

def sobre(request):
    return render(request, 'html/sobre.html')


@login_required
def adm(request):
   return render(request, 'html/adm.html')

@login_required
def user(request):
   return render(request, 'html/user.html')