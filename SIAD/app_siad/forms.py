from django import forms
from django.contrib.auth.models import User
from .models import RepresentanteEsportivo
from django.contrib.auth.forms import AuthenticationForm

def validar_cpf(cpf):
    cpf = ''.join([char for char in cpf if char.isdigit()])  # Remove qualquer caractere que não seja dígito
    if len(cpf) != 11:
        return False

    if cpf in [s * 11 for s in "0123456789"]:
        return False  # CPFs com todos os dígitos iguais são inválidos

    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    primeiro_verificador = (soma * 10 % 11) % 10
    if primeiro_verificador != int(cpf[9]):
        return False

    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    segundo_verificador = (soma * 10 % 11) % 10
    if segundo_verificador != int(cpf[10]):
        return False

    return True

class RepresentanteRegistroForm(forms.ModelForm):
    username = forms.CharField(label="CPF", max_length=11)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    nome = forms.CharField(label="Nome", max_length=100)
    telefone = forms.CharField(label="Telefone", max_length=20)
    documento = forms.FileField(label="Termo de Compromisso Assinado")
    rg = forms.CharField(label="RG", max_length=20)
    dados_escola = forms.CharField(label="Dados da Escola", widget=forms.Textarea)

    class Meta:
        model = RepresentanteEsportivo
        fields = ['nome', 'telefone', 'email', 'documento', 'rg', 'dados_escola']

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