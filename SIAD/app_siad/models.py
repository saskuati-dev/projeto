from django.db import models
from django.contrib.auth.models import User

class EventoOriginal(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self):
        return self.nome
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
    evento_original = models.ForeignKey('EdicaoEvento', on_delete=models.CASCADE)
    def __str__(self):
        return self.nome + ' ' +self.categoria

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

class Divisao(models.Model):
    tipo= {
        ('G', 'Grupo'),
        ('I', 'Individual')
    }
    minAtleta = models.PositiveIntegerField(default=1)
    maxAtleta = models.PositiveIntegerField(default=1)
    tipo_divisao = models.CharField(max_length=1,default='', choices=tipo)
    modalidade = models.ForeignKey(EdicaoEvento, on_delete=models.CASCADE)

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

class AtletaGrupoDivisao(models.Model):
    atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    divisao = models.ForeignKey(Divisao, on_delete=models.CASCADE)


class RepresentanteEsportivo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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