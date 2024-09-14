from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
import datetime


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    imagem = models.ImageField(upload_to='noticias/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']  
    def __str__(self):
        return self.titulo

class EventoOriginal(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
    

class EdicaoEvento(models.Model):
    edicao = models.CharField(max_length=50)
    local = models.CharField(max_length=100)
    descricao = models.TextField()
    cidade = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    evento_original = models.ForeignKey(EventoOriginal, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.evento_original) +' '+str(self.edicao)
    
class Modalidade(models.Model):
    genero= {
        ('Fem.', 'Feminino'),
        ('Masc.', 'Masculino'),
        ('Geral','Geral')
    }
    nome = models.CharField(max_length=100)
    regras_modalidade = models.TextField()
    local = models.CharField(max_length=100)
    categoria = models.CharField(max_length=5,default='', choices=genero)
    edicao_evento = models.ForeignKey(EdicaoEvento, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome + ' ' +self.categoria



class Divisao(models.Model):
    tipo= {
        ('G', 'Grupo'),
        ('I', 'Individual')
    }
    minAtleta = models.PositiveIntegerField(default=1)
    maxAtleta = models.PositiveIntegerField(default=1)
    tipo_divisao = models.CharField(max_length=1,default='', choices=tipo)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)

class Atleta(models.Model):
    nome = models.CharField(max_length=100)
    nascimento = models.DateField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=11, unique=True)
    comprovante_matricula = models.FileField(upload_to='comprovantes_matricula/')
   

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao_grupo = models.TextField()
    taxa = models.DecimalField(max_digits=10, decimal_places=2)
    edicao_evento = models.ForeignKey(EdicaoEvento, related_name='grupos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class AtletaGrupoDivisao(models.Model):
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    divisao = models.ForeignKey(Divisao, on_delete=models.CASCADE)


class RepresentanteEsportivo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    representacao = models.CharField(max_length=150, unique=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, unique=True)
    documento = models.FileField(upload_to="comprovantes_matricula/")  
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    dados_escola = models.TextField()

    def __str__(self):
        return self.nome

class Pagamentos(models.Model):
    qtd_atletas = models.PositiveIntegerField()
    comprovante = models.FileField(upload_to='comprovantes/', blank=True, null=True)
    equipe = models.ForeignKey('Equipe', on_delete=models.CASCADE)

class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    representante_esportivo = models.ForeignKey(RepresentanteEsportivo, on_delete=models.CASCADE)



def get_upload_to(instance, filename):
    # Acessa o modelo EdicaoEvento para obter o nome do evento
    evento_nome = instance.evento.edicao  # ou outro atributo do EdicaoEvento que você deseja usar
    data_atual = datetime.datetime.now().strftime('%Y%m%d')
    nome_arquivo, extensao = os.path.splitext(filename)
    novo_nome_arquivo = f"{data_atual}_{nome_arquivo}{extensao}"
    return f"eventos/{evento_nome}/{novo_nome_arquivo}"

class Edital(models.Model):
    evento = models.ForeignKey('EdicaoEvento', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to=get_upload_to)