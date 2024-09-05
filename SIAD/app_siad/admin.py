from django.contrib import admin
from .models import EventoOriginal, Modalidade, EdicaoEvento, Divisao, Atleta, Grupo, AtletaGrupoDivisao, RepresentanteEsportivo, Pagamentos, Equipe


@admin.register(EventoOriginal)
class EventoOriginalAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'local', 'evento_original')
    search_fields = ('nome', 'local')
    list_filter = ('evento_original',)

@admin.register(EdicaoEvento)
class EdicaoEventoAdmin(admin.ModelAdmin):
    list_display = ('local', 'descricao', 'cidade', 'data_inicio', 'data_fim', 'evento_original')
    search_fields = ('local', 'cidade', 'descricao')
    list_filter = ('data_inicio', 'data_fim', 'evento_original')

@admin.register(Divisao)
class DivisaoAdmin(admin.ModelAdmin):
    list_display = ('tipo_divisao',)
    search_fields = ('tipo_divisao',)
    list_filter = ('tipo_divisao',)

@admin.register(Atleta)
class AtletaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nascimento', 'rg', 'cpf')
    search_fields = ('nome', 'cpf')
    list_filter = ('nascimento',)

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao_grupo', 'taxa')
    search_fields = ('nome',)
    list_filter = ('taxa',)

@admin.register(AtletaGrupoDivisao)
class AtletaGrupoDivisaoAdmin(admin.ModelAdmin):
    list_display = ('atleta', 'grupo', 'divisao')
    list_filter = ('divisao', 'grupo', 'atleta')

@admin.register(RepresentanteEsportivo)
class RepresentanteEsportivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'documento', 'cpf', 'rg')
    search_fields = ('nome', 'cpf', 'rg')
    list_filter = ('dados_escola',)

@admin.register(Pagamentos)
class PagamentosAdmin(admin.ModelAdmin):
    list_display = ('qtd_atletas', 'equipe')
    search_fields = ('equipe__nome',)
    list_filter = ('equipe',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'representante_esportivo')
    search_fields = ('nome',)
    list_filter = ('representante_esportivo',)
