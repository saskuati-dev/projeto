from gerencianet import Gerencianet
from django.conf import settings

def criar_cobranca_pix(valor, nome, email):
    # Configurações do Gerencianet
    credentials = {
        'client_id': settings.GERENCIANET_CLIENT_ID,
        'client_secret': settings.GERENCIANET_CLIENT_SECRET,
        'sandbox': True  # Usar True para ambiente de testes, False para produção
    }

    # Instanciando o cliente do Gerencianet
    gn = Gerencianet(credentials)

    # Dados da cobrança
    params = {
        'valor': str(valor),  # Valor da cobrança
        'descricao': 'Pagamento via PIX',  # Descrição do pagamento
        'nome': nome,
        'email': email,
    }

    # Criando a cobrança
    try:
        response = gn.create_charge(params)
        return response
    except Exception as e:
        print(f"Erro ao criar cobrança: {e}")
        return None

def consultar_status_pix(id_cobranca):
    # Consultando o status do pagamento
    credentials = {
        'client_id': settings.GERENCIANET_CLIENT_ID,
        'client_secret': settings.GERENCIANET_CLIENT_SECRET,
        'sandbox': True
    }

    gn = Gerencianet(credentials)

    try:
        response = gn.get_charge(id_cobranca)
        return response
    except Exception as e:
        print(f"Erro ao consultar o status do pagamento: {e}")
        return None
