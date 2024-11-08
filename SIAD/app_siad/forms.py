from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from tinymce.widgets import TinyMCE
from .models import Atleta,Edital,EdicaoEvento, EventoOriginal, Noticia, RepresentanteEsportivo, EdicaoEvento, Grupo, Modalidade, Divisao
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError



class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'nascimento', 'rg', 'cpf', 'comprovante_matricula']


        
class EditalForm(forms.ModelForm):
    class Meta:
        model = Edital
        fields = ['arquivo']

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if not arquivo.name.endswith('.pdf'):
            raise forms.ValidationError("O arquivo deve ser um PDF.")
        return arquivo
    
class DivisaoForm(forms.ModelForm):
    class Meta:
        model = Divisao
        fields = ['tipo_divisao', 'minAtleta', 'maxAtleta', 'modalidade']

    # Campo oculto para associar a divisão ao grupo
    grupo_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()

        min_atleta = cleaned_data.get('minAtleta')
        max_atleta = cleaned_data.get('maxAtleta')

        # Verifica se maxAtleta é maior que minAtleta
        if min_atleta is not None and max_atleta is not None:
            if max_atleta <= min_atleta:
                raise forms.ValidationError("O número máximo de atletas deve ser maior que o número mínimo.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        grupo_id = kwargs.pop('grupo_id', None)
        super().__init__(*args, **kwargs)

        # Se o grupo_id for passado, preenche o campo oculto
        if grupo_id:
            self.fields['grupo_id'].initial = grupo_id

    def save(self, commit=True):
        divisao = super().save(commit=False)
        grupo_id = self.cleaned_data.get('grupo_id')

        # Se o grupo_id foi passado, associamos a divisão ao grupo
        if grupo_id:
            grupo = Grupo.objects.get(id=grupo_id)
            divisao.grupo = grupo

        if commit:
            divisao.save()

        return divisao
class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'regras_modalidade', 'local', 'categoria']

        def clean(self):
            nome = self.cleaned_data.get('nome')
            return nome.upper() if nome else nome
class EventoOriginalForm(forms.ModelForm):
    class Meta:
        model = EventoOriginal
        fields = ['nome']

class EdicaoEventoForm(forms.ModelForm):
    
    evento_original = forms.ModelChoiceField(
        queryset=EventoOriginal.objects.all(),
        empty_label="Escolha um evento original ou crie um novo",
        required=False
    )
    novo_evento_original = forms.CharField(
        max_length=100,
        required=False,
        label="Criar novo evento original"
    )
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    data_fim_inscricao = forms.DateField(
        label="Data final para inscrição:",
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=settings.DATE_INPUT_FORMATS
    )
    
    class Meta:
        model = EdicaoEvento
        fields = ['edicao', 'local', 'descricao', 'cidade', 'data_inicio', 'data_fim', 'data_fim_inscricao']

    def clean(self):
        cleaned_data = super().clean()
        data_fim_inscricao = cleaned_data.get('data_fim_inscricao')  # Acessando o campo correto
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        # Verificação da data de fim da inscrição
        if not data_fim_inscricao:
            raise forms.ValidationError("O campo 'Data final para inscrição' é obrigatório.")  # Verificando se o campo é preenchido

        if data_fim_inscricao and data_inicio and data_fim:
            if data_inicio >= data_fim_inscricao:
                raise forms.ValidationError("A data final de inscrição não pode ser anterior à data de início.")
            if data_fim_inscricao >= data_fim:
                raise forms.ValidationError("A data final de inscrição não pode ser posterior à data final do evento.")

        return cleaned_data

class GrupoForm(forms.ModelForm):
    taxa = forms.DecimalField(
        label="Taxa (R$):",
        max_digits=10,
        decimal_places=2,
        localize=True
    )
    class Meta:
        
        model = Grupo
        fields = ['nome', 'descricao_grupo', 'taxa']
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        # Converte o nome para maiúsculas
        nome_upper = nome.upper()

        # Verifica se já existe algum grupo com o nome em maiúsculas
        if Grupo.objects.filter(nome=nome_upper).exists():
            raise ValidationError(f"Já existe um grupo com o nome '{nome_upper}'.")
        
        return nome_upper

    # Sobrescrevendo o método clean() para garantir que o nome seja armazenado em maiúsculas
    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')

        if nome:
            # Converte o nome para maiúsculas
            cleaned_data['nome'] = nome.upper()

        return cleaned_data
        
def validar_cpf(cpf):
    cpf = ''.join([char for char in cpf if char.isdigit()])  
    if len(cpf) != 11:
        return False

    if cpf in [s * 11 for s in "0123456789"]:
        return False  
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_verificador = (soma * 10 % 11) % 10
    if primeiro_verificador != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_verificador = (soma * 10 % 11) % 10
    if segundo_verificador != int(cpf[10]):
        return False

    return True

class RepresentanteRegistroForm(forms.ModelForm):
    username = forms.CharField(label="CPF:", max_length=11)
    representacao = forms.CharField(label="Representação:")
    email = forms.EmailField(label="Email:")
    password = forms.CharField(label="Senha:", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirme a Senha: ", widget=forms.PasswordInput)    
    nome = forms.CharField(label="Nome:", max_length=100)
    telefone = forms.CharField(label="Telefone:", max_length=20)
    documento = forms.FileField(label="Termo de Compromisso Assinado:")
    rg = forms.CharField(label="RG:", max_length=20)
    dados_escola = forms.CharField(label="Detalhes:",  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

    class Meta:
        model = RepresentanteEsportivo
        fields = ['nome', 'representacao','telefone', 'email', 'documento', 'rg', 'dados_escola']

    def clean_username(self):
        cpf = self.cleaned_data.get('username')
        if not validar_cpf(cpf):
            raise forms.ValidationError("CPF inválido.")
        if User.objects.filter(username=cpf).exists():
            raise forms.ValidationError("CPF já cadastrado.")
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RepresentanteEsportivo.objects.filter(email=email).exists():
            raise forms.ValidationError("Email já cadastrado.")
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if RepresentanteEsportivo.objects.filter(telefone=telefone).exists():
            raise forms.ValidationError("Telefone já cadastrado.")
        return telefone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("As senhas são diferentes.")

        return cleaned_data
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        representante = super().save(commit=False)
        representante.user = user
        if commit:
            representante.save()
        return representante


class RepresentanteLoginForm(AuthenticationForm):
    username = forms.CharField(label="CPF", max_length=11)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)



class NoticiaForm(forms.ModelForm):
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=settings.DATE_INPUT_FORMATS
    )

    class Meta:
        model = Noticia
        fields = ['titulo', 'texto', 'imagem', 'data_fim']
        widgets = {
            'texto': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        data_fim = cleaned_data.get('data_fim')
        if data_fim < timezone.now().date():
            raise forms.ValidationError("A data de expiração da noticia deve ser hoje ou uma data futura.")