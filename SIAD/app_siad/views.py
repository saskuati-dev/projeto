from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .forms import RepresentanteLoginForm, RepresentanteRegistroForm
import logging
import os
from django.conf import settings
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






def editais(request):
    # Caminho para a pasta de eventos
    eventos_path = os.path.join(settings.MEDIA_ROOT, 'eventos')

    eventos = []
    if os.path.exists(eventos_path):
        # Para cada diretório dentro de 'eventos' (que representa um evento)
        for nome_evento in sorted(os.listdir(eventos_path), key=lambda x: os.path.getmtime(os.path.join(eventos_path, x)), reverse=True):
            evento_path = os.path.join(eventos_path, nome_evento)

            # Verifica se é um diretório (evento)
            if os.path.isdir(evento_path):
                # Lista os arquivos de editais dentro da pasta do evento, ordenados por data de modificação
                editais = sorted(
                    [edital for edital in os.listdir(evento_path) if os.path.isfile(os.path.join(evento_path, edital))],
                    key=lambda x: os.path.getmtime(os.path.join(evento_path, x)),
                    reverse=True
                )

                # Adiciona o evento e seus editais à lista de eventos
                eventos.append({
                    'nome': nome_evento,  # Nome do evento
                    'editais': [
                        {
                            'nome': edital,
                            'url': os.path.join(settings.MEDIA_URL, 'eventos', nome_evento, edital)
                        }
                        for edital in editais
                    ],
                })

    return render(request, 'html/editais.html', {'eventos': eventos})