from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .forms import RepresentanteLoginForm, RepresentanteRegistroForm, NoticiaForm, EdicaoEventoForm, GrupoForm
from .models import Noticia, EdicaoEvento, Grupo, EventoOriginal
import logging
import os
from django.conf import settings
from django.http import HttpResponseForbidden

def add_grupos(request, evento_id):
    evento = get_object_or_404(EdicaoEvento, id=evento_id)

    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.edicao_evento = evento
            grupo.save()
            return redirect('add_grupos', evento_id=evento_id)
    else:
        form = GrupoForm()

    return render(request, 'html/add_grupos.html', {'form': form, 'evento': evento})

def delete_grupos(request, evento_id):
    evento = get_object_or_404(EdicaoEvento, id=evento_id)

    if request.method == 'POST':
        grupo_ids = request.POST.getlist('grupos')
        Grupo.objects.filter(id__in=grupo_ids).delete()
        return redirect('adm')

    grupos = Grupo.objects.filter(edicao_evento=evento)
    return render(request, 'html/delete_grupos.html', {'grupos': grupos, 'evento': evento})

def detalhes_grupo(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    return render(request, 'html/detalhes_grupo.html', {'grupo': grupo})
def criar_evento(request):
    if request.method == 'POST':
        form = EdicaoEventoForm(request.POST)
        num_grupos = int(request.POST.get('num_grupos', 0))

        if form.is_valid():
            evento_data = form.cleaned_data
            evento_original = evento_data['evento_original']
            novo_evento_original = evento_data['novo_evento_original']
            
            if not evento_original:
                evento_original = EventoOriginal.objects.create(nome=novo_evento_original)
            
            edicao_evento = EdicaoEvento.objects.create(
                edicao=form.cleaned_data['edicao'],
                local=form.cleaned_data['local'],
                descricao=form.cleaned_data['descricao'],
                cidade=form.cleaned_data['cidade'],
                data_inicio=form.cleaned_data['data_inicio'],
                data_fim=form.cleaned_data['data_fim'],
                evento_original=evento_original
            )
            
            evento_folder = os.path.join(settings.MEDIA_ROOT, 'eventos', str(edicao_evento.edicao))
            if not os.path.exists(evento_folder):
                os.makedirs(evento_folder)

            # Processar formulários de grupos


            request.session['edicao_evento_id'] = edicao_evento.id
            return redirect('adm')
    else:
        form = EdicaoEventoForm()
        num_grupos = 0

    return render(request, 'html/criar_evento.html', {'form': form, 'num_grupos': num_grupos})



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


#@login_required(login_url='login')
def adm(request): 
    #if not is_admin_esportivo(request.user):
     #   logout(request)
      #  return redirect('home')
    
    eventos = EdicaoEvento.objects.all()
    print(eventos)
    return render(request, 'html/adm.html', {'eventos': eventos})





@login_required(login_url='login')
def eventos_view(request):
    if not is_admin_esportivo(request.user):
        return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
    
    if request.method == 'POST':
        form = EdicaoEventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('html/eventos_view')  
    else:
        form = EdicaoEventoForm()
    
    eventos = EdicaoEvento.objects.all()
    return render(request, 'html/eventos.html', {'form': form, 'eventos': eventos})


def home(request):
    
    noticias = Noticia.objects.all().order_by('-criado_em')
    return render(request, 'html/home.html', {'noticias': noticias})


def sobre(request):
    return render(request, 'html/sobre.html')


def editais(request):
    eventos_path = os.path.join(settings.MEDIA_ROOT, 'eventos')

    eventos = []
    if os.path.exists(eventos_path):
        for nome_evento in sorted(os.listdir(eventos_path), key=lambda x: os.path.getmtime(os.path.join(eventos_path, x)), reverse=True):
            evento_path = os.path.join(eventos_path, nome_evento)

            if os.path.isdir(evento_path):
                editais = sorted(
                    [edital for edital in os.listdir(evento_path) if os.path.isfile(os.path.join(evento_path, edital))],
                    key=lambda x: os.path.getmtime(os.path.join(evento_path, x)),
                    reverse=True
                )

                eventos.append({
                    'nome': nome_evento,
                    'editais': [
                        {
                            'nome': edital,
                            'url': os.path.join(settings.MEDIA_URL, 'eventos', nome_evento, edital)
                        }
                        for edital in editais
                    ],
                })

    return render(request, 'html/editais.html', {'eventos': eventos})


def noticias(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = NoticiaForm()
    return render(request, 'html/noticias.html', {'form': form})



