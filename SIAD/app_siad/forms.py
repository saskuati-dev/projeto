from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from tinymce.widgets import TinyMCE
from .models import Atleta,Edital,EdicaoEvento, EventoOriginal, Noticia, RepresentanteEsportivo, EdicaoEvento, Grupo, Modalidade, Divisao


class InscricaoDivisaoForm(forms.Form):
    atleta = forms.ModelChoiceField(queryset=Atleta.objects.none(), label='Atleta')
    divisao = forms.ModelChoiceField(queryset=Divisao.objects.none(), label='Divisão')

    def __init__(self, *args, **kwargs):
        grupo_id = kwargs.pop('grupo_id', None)
        super().__init__(*args, **kwargs)

        if grupo_id:
            
            self.fields['atleta'].queryset = Atleta.objects.filter(
                atletagrupodivisao__grupo__id=grupo_id
            ).distinct()


            self.fields['divisao'].queryset = Divisao.objects.filter(
                modalidade__edicao_evento__grupos__id=grupo_id
            ).distinct()



class AtletaDivisaoForm(forms.Form):
    atletas = forms.ModelMultipleChoiceField(
        queryset=Atleta.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Atletas'
    )

class AtletaForm(forms.ModelForm):
    class Meta:
        model = Atleta
        fields = ['nome', 'nascimento', 'rg', 'cpf', 'comprovante_matricula']
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Atleta.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Já existe um atleta com este CPF.")
        return cpf

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona um queryset personalizado se necessário
        self.fields['modalidade'].queryset = Modalidade.objects.all()

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome', 'regras_modalidade', 'local', 'categoria']

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

    class Meta:
        model = EdicaoEvento
        fields = ['edicao', 'local', 'descricao', 'cidade', 'data_inicio', 'data_fim']

    def clean(self):
        cleaned_data = super().clean()
        evento_original = cleaned_data.get('evento_original')
        novo_evento_original = cleaned_data.get('novo_evento_original')

        if not evento_original and not novo_evento_original:
            raise forms.ValidationError("Você deve escolher um evento original ou criar um novo.")

        if not evento_original and novo_evento_original:
            if EventoOriginal.objects.filter(nome=novo_evento_original).exists():
                raise forms.ValidationError("Um evento original com esse nome já existe.")

        return cleaned_data
    
class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao_grupo', 'taxa']
        
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
    username = forms.CharField(label="CPF", max_length=11)
    representacao = forms.CharField(label="Representação:")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    nome = forms.CharField(label="Nome", max_length=100)
    telefone = forms.CharField(label="Telefone", max_length=20)
    documento = forms.FileField(label="Termo de Compromisso Assinado")
    rg = forms.CharField(label="RG", max_length=20)
    dados_escola = forms.CharField(label="Dados da Escola",  widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

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
    class Meta:
        model = Noticia
        fields = ['titulo', 'texto', 'imagem']
        widgets = {
            'texto': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }