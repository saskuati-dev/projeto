from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .forms import RepresentanteLoginForm, RepresentanteRegistroForm, NoticiaForm, EditalForm,EdicaoEventoForm, GrupoForm, ModalidadeForm, DivisaoForm
from .models import Noticia, EdicaoEvento, Grupo, EventoOriginal, Modalidade, Divisao
import logging
import os
from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib import messages


@login_required(login_url='login')
def evento_detalhes(request, evento_id):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    evento = get_object_or_404(EdicaoEvento, id=evento_id)
    
    grupos = Grupo.objects.filter(edicao_evento=evento)
    modalidades = Modalidade.objects.filter(edicao_evento=evento)
    divisoes = Divisao.objects.filter(modalidade__edicao_evento=evento)
    
    if request.method == 'POST':
        # Handle group form submissions
        if 'add_grupo' in request.POST:
            form = GrupoForm(request.POST)
            if form.is_valid():
                grupo = form.save(commit=False)
                grupo.edicao_evento = evento
                grupo.save()
                messages.success(request, "Grupo adicionado com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'edit_grupo' in request.POST:
            grupo_id = request.POST.get('grupo_id')
            grupo = get_object_or_404(Grupo, id=grupo_id)
            form = GrupoForm(request.POST, instance=grupo)
            if form.is_valid():
                form.save()
                messages.success(request, "Grupo editado com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'delete_grupo' in request.POST:
            grupo_id = request.POST.get('grupo_id')
            grupo = get_object_or_404(Grupo, id=grupo_id)
            grupo.delete()
            messages.success(request, "Grupo removido com sucesso!")
            return redirect('detalhes_evento', evento_id=evento_id)
        
        # Handle modality form submissions
        if 'add_modalidade' in request.POST:
            form = ModalidadeForm(request.POST)
            if form.is_valid():
                modalidade = form.save(commit=False)
                modalidade.edicao_evento = evento
                modalidade.save()
                messages.success(request, "Modalidade adicionada com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'edit_modalidade' in request.POST:
            modalidade_id = request.POST.get('modalidade_id')
            modalidade = get_object_or_404(Modalidade, id=modalidade_id)
            form = ModalidadeForm(request.POST, instance=modalidade)
            if form.is_valid():
                form.save()
                messages.success(request, "Modalidade editada com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'delete_modalidade' in request.POST:
            modalidade_id = request.POST.get('modalidade_id')
            modalidade = get_object_or_404(Modalidade, id=modalidade_id)
            modalidade.delete()
            messages.success(request, "Modalidade removida com sucesso!")
            return redirect('detalhes_evento', evento_id=evento_id)
        
        # Handle division form submissions
        if 'add_divisao' in request.POST:
            form = DivisaoForm(request.POST)
            if form.is_valid():
                divisao = form.save(commit=False)
                # Modalidade is already handled as ID by the form
                divisao.save()
                messages.success(request, "Divisão adicionada com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'edit_divisao' in request.POST:
            divisao_id = request.POST.get('divisao_id')
            divisao = get_object_or_404(Divisao, id=divisao_id)
            form = DivisaoForm(request.POST, instance=divisao)
            if form.is_valid():
                form.save()
                messages.success(request, "Divisão editada com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'delete_divisao' in request.POST:
            divisao_id = request.POST.get('divisao_id')
            divisao = get_object_or_404(Divisao, id=divisao_id)
            divisao.delete()
            messages.success(request, "Divisão removida com sucesso!")
            return redirect('detalhes_evento', evento_id=evento_id)
    
    else:
        grupo_form = GrupoForm()
        modalidade_form = ModalidadeForm()
        divisao_form = DivisaoForm()

    context = {
        'evento': evento,
        'grupos': grupos,
        'modalidades': modalidades,
        'divisoes': divisoes,
        'grupo_form': grupo_form,
        'modalidade_form': modalidade_form,
        'divisao_form': divisao_form,
    }

    return render(request, 'html/detalhes_evento.html', context)



@login_required(login_url='login')
def upload_edital(request, evento_id):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    
    evento = get_object_or_404(EdicaoEvento, id=evento_id)

    if request.method == 'POST':
        form = EditalForm(request.POST, request.FILES)
        if form.is_valid():
            edital = form.save(commit=False)
            edital.evento = evento  # Associa o edital ao evento
            edital.save()
            return redirect('editais')  # Redireciona para a lista de editais ou outra página apropriada
    else:
        form = EditalForm()

    return render(request, 'html/upload_edital.html', {'form': form, 'evento': evento})

@login_required(login_url='login')
def detalhes_grupo(request, pk):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    grupo = get_object_or_404(Grupo, pk=pk)
    return render(request, 'html/detalhes_grupo.html', {'grupo': grupo})

@login_required(login_url='login')
def criar_evento(request):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    if request.method == 'POST':
        form = EdicaoEventoForm(request.POST)
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
            num_grupos = int(request.POST.get('num_grupos', 0))
            for i in range(num_grupos):
                grupo_nome = request.POST.get(f'grupo_nome_{i}')
                grupo_descricao = request.POST.get(f'grupo_descricao_{i}')
                grupo_taxa = request.POST.get(f'grupo_taxa_{i}')
                if grupo_nome:
                    Grupo.objects.create(
                        nome=grupo_nome,
                        descricao_grupo=grupo_descricao,
                        taxa=grupo_taxa,
                        edicao_evento=edicao_evento
                    )
            
            request.session['edicao_evento_id'] = edicao_evento.id
            return redirect('adm')
    else:
        form = EdicaoEventoForm()
    
    return render(request, 'html/criar_evento.html', {'form': form})



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
    
    eventos = EdicaoEvento.objects.all()
    
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



