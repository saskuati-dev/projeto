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
from django.contrib import messages
from django.utils import timezone
import shutil
import json





@login_required(login_url='login')
def evento_detalhes(request, evento_id):
    # Verificar se o usuário tem permissão de administrador
    if not is_admin_esportivo(request.user):
        return redirect('home')
    
    # Buscar evento, grupos, modalidades e divisões
    evento = get_object_or_404(EdicaoEvento, id=evento_id)
    grupos = Grupo.objects.filter(edicao_evento=evento)
    modalidades = Modalidade.objects.filter(edicao_evento=evento)
    
    # Inicializar os formulários
    grupo_form = GrupoForm()
    modalidade_form = ModalidadeForm()

    # Verificar se a requisição é POST para manipular os formulários
    if request.method == 'POST':
        # Manipulação de Grupo
        if 'add_grupo' in request.POST:
            grupo_form = GrupoForm(request.POST)
            if grupo_form.is_valid():
                grupo = grupo_form.save(commit=False)
                grupo.edicao_evento = evento
                grupo.save()
                messages.success(request, "Grupo adicionado com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'edit_grupo' in request.POST:
            grupo_id = request.POST.get('grupo_id')
            grupo = get_object_or_404(Grupo, id=grupo_id)
            grupo_form = GrupoForm(request.POST, instance=grupo)
            if grupo_form.is_valid():
                grupo_form.save()
                messages.success(request, "Grupo editado com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'delete_grupo' in request.POST:
            grupo_id = request.POST.get('grupo_id')
            grupo = get_object_or_404(Grupo, id=grupo_id)
            grupo.delete()
            messages.success(request, "Grupo removido com sucesso!")
            return redirect('detalhes_evento', evento_id=evento_id)
        
        # Manipulação de Modalidade
        elif 'add_modalidade' in request.POST:
            modalidade_form = ModalidadeForm(request.POST)
            if modalidade_form.is_valid():
                modalidade = modalidade_form.save(commit=False)
                modalidade.edicao_evento = evento
                modalidade.save()
                messages.success(request, "Modalidade adicionada com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'edit_modalidade' in request.POST:
            modalidade_id = request.POST.get('modalidade_id')
            modalidade = get_object_or_404(Modalidade, id=modalidade_id)
            modalidade_form = ModalidadeForm(request.POST, instance=modalidade)
            if modalidade_form.is_valid():
                modalidade_form.save()
                messages.success(request, "Modalidade editada com sucesso!")
                return redirect('detalhes_evento', evento_id=evento_id)
        
        elif 'delete_modalidade' in request.POST:
            modalidade_id = request.POST.get('modalidade_id')
            modalidade = get_object_or_404(Modalidade, id=modalidade_id)
            modalidade.delete()
            messages.success(request, "Modalidade removida com sucesso!")
            return redirect('detalhes_evento', evento_id=evento_id)

        # Manipulação de Exclusão do Evento
        elif 'delete_evento' in request.POST:
            evento.delete()
            evento_folder = os.path.join(settings.MEDIA_ROOT, 'eventos', str(evento.edicao))  # Considerando que 'evento' tem o campo 'edicao'

            if os.path.exists(evento_folder) and os.path.isdir(evento_folder):
                shutil.rmtree(evento_folder)
            return redirect('adm')
        
        elif  'action' in request.POST and request.POST['action'] == 'delete':
            # Pegar os IDs dos grupos selecionados
            grupo_ids = request.POST.getlist('grupos')
            if grupo_ids:
                # Excluir os grupos selecionados
                grupos_a_excluir = Grupo.objects.filter(id__in=grupo_ids, edicao_evento=evento)
                grupos_a_excluir.delete()
                messages.success(request, "Grupos selecionados foram excluídos com sucesso!")
            else:
                messages.warning(request, "Nenhum grupo foi selecionado para exclusão.")
            
            # Redirecionar de volta para a página de detalhes do evento
            return redirect('detalhes_evento', evento_id=evento_id)
        
        if 'delete_modalidade' in request.POST:
            modalidade_id = request.POST.get('modalidade_id')
            if modalidade_id:
                modalidade = get_object_or_404(Modalidade, id=modalidade_id)
                modalidade.delete()
                messages.success(request, "Modalidade excluída com sucesso!")
            return redirect('detalhes_evento', evento_id=evento_id)
        
    context = {
        'evento': evento,
        'grupos': grupos,
        'modalidades': modalidades,
        'grupo_form': grupo_form,
        'modalidade_form': modalidade_form,
    }

    return render(request, 'html/detalhes_evento.html', context)

def excluir_evento(request, evento_id):
    # Obter o evento
    evento = get_object_or_404(EdicaoEvento, id=evento_id)

    if request.method == 'POST':
        # Verificar se o usuário confirmou a exclusão
        if 'confirmar' in request.POST and request.POST['confirmar'] == 'sim':
            # Excluir o evento
            evento.delete()

            # Deletar a pasta do evento
            evento_folder = os.path.join(settings.MEDIA_ROOT, 'eventos', str(evento.edicao))
            if os.path.exists(evento_folder) and os.path.isdir(evento_folder):
                shutil.rmtree(evento_folder)

            # Redirecionar para a página de administração após a exclusão
            return redirect('adm')

        # Se o usuário não confirmou, redireciona de volta
        return redirect('adm')

    return render(request, 'html/excluir_evento.html', {'evento': evento})

@login_required(login_url='login')
def detalhes_user(request, grupo_id, evento_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    evento = get_object_or_404(EdicaoEvento, id=evento_id)
    
    # Filtra as divisões associadas ao grupo específico
    divisoes = Divisao.objects.filter(grupo=grupo)

    return render(request, 'html/grupo_user.html', {
        'grupo': grupo,
        'evento': evento,
        'divisoes': divisoes  # Divisões associadas ao grupo
    })
    
@login_required(login_url='login')
def upload_edital(request, evento_id):
    if not is_admin_esportivo(request.user):
        return redirect('home')
    
    evento = get_object_or_404(EdicaoEvento, id=evento_id)

    if request.method == 'POST':
        form = EditalForm(request.POST, request.FILES)
        if form.is_valid():
            edital = form.save(commit=False)
            edital.evento = evento  
            edital.save()
            return redirect('editais')  
    else:
        form = EditalForm()

    context = {
        'form': form,
        'evento': evento
    }
    
    return render(request, 'html/upload_edital.html', context)

@login_required(login_url='login')
def detalhes_grupo(request, grupo_id, evento_id):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    
    # Recupera o evento e o grupo
    evento = get_object_or_404(EdicaoEvento, id=evento_id)
    grupo = get_object_or_404(Grupo, id=grupo_id)

    # Filtra as divisões associadas ao grupo
    divisoes_do_grupo = Divisao.objects.filter(grupo=grupo)

    # Recupera as modalidades do evento
    modalidades = Modalidade.objects.filter(edicao_evento=evento)

    # Retorna o contexto com as divisões associadas ao grupo
    return render(request, 'html/detalhes_grupo.html', {
        'grupo': grupo,
        'divisoes_do_grupo': divisoes_do_grupo,  # Divisões associadas ao grupo
        'evento': evento,
        'modalidades': modalidades
    })


@login_required(login_url='login')
def editar_divisoes(request, grupo_id, evento_id):
    if not is_admin_esportivo(request.user):
        logout(request)
        return redirect('home')
    
    evento = get_object_or_404(EdicaoEvento, id=evento_id)
    grupo = get_object_or_404(Grupo, id=grupo_id)

    modalidades = Modalidade.objects.filter(edicao_evento=evento)
    divisoes = Divisao.objects.filter(grupo=grupo)

    # Inicializar o formulário sempre, mesmo antes de qualquer ação
    divisao_form = DivisaoForm(grupo_id=grupo.id)

    if request.method == 'POST':
        # Verificando se o botão de exclusão foi pressionado
        if 'action' in request.POST and request.POST['action'] == 'delete':
            divisao_ids = request.POST.getlist('divisoes')  # Obtém os IDs das divisões selecionadas

            if divisao_ids:
                divisoes_para_apagar = Divisao.objects.filter(id__in=divisao_ids)
                divisoes_para_apagar.delete()
                messages.success(request, 'Divisões excluídas com sucesso!')
            else:
                messages.error(request, 'Nenhuma divisão selecionada para exclusão.')

            # Não precisamos recarregar o formulário de divisão, pois já o inicializamos
            return redirect('editar_divisoes', grupo_id=grupo.id, evento_id=evento.id)

        # Processo para adicionar ou editar a divisão
        else:
            divisao_form = DivisaoForm(request.POST, grupo_id=grupo.id)
            if divisao_form.is_valid():
                divisao_form.save()
                messages.success(request, 'Divisão salva com sucesso!')
                return redirect('editar_divisoes', grupo_id=grupo.id, evento_id=evento.id)

    # Se o método for GET ou após uma submissão, o formulário será renderizado com a instância
    return render(request, 'html/editar_divisoes.html', {
        'grupo': grupo,
        'evento': evento,
        'divisoes': divisoes,
        'modalidades': modalidades,
        'divisao_form': divisao_form,
    })


@login_required(login_url='login')
def criar_evento(request):
    if not is_admin_esportivo(request.user):
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
                data_fim_inscricao=form.cleaned_data['data_fim_inscricao'],
                evento_original=evento_original
            )
            
            evento_folder = os.path.join(settings.MEDIA_ROOT, 'eventos', str(edicao_evento.edicao))
            if not os.path.exists(evento_folder):
                os.makedirs(evento_folder)

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
            return redirect('gerenciar')  
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
        return redirect('home')
    eventos = EdicaoEvento.objects.all()
    
    context = {
        'eventos': eventos,
    }
    return render(request, 'html/user.html', context)
    

@login_required(login_url='login')
def adm(request): 
    if not is_admin_esportivo(request.user):
        return redirect('user')
    
    eventos = EdicaoEvento.objects.all()
    
    return render(request, 'html/adm.html', {'eventos': eventos})

@login_required(login_url='login')
def eventos_view(request):
    if not is_admin_esportivo(request.user):
        return redirect("home")
    
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
    noticias = Noticia.objects.filter(data_fim__gt=timezone.now())
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


   

@login_required(login_url='login')
def noticias(request):
    if not is_admin_esportivo(request.user):
        return redirect('home')
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = NoticiaForm()
    return render(request, 'html/noticias.html', {'form': form})



@login_required(login_url='login')
def gerenciar(request):
     if not is_representante_esportivo(request.user):
        return redirect('adm')
        
     return redirect('user')



@login_required(login_url='login')
def inscricao(request, evento_id, grupo_id):
    
    return render(request, 'html/inscricao.html')