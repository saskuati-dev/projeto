from gerencianet import Gerencianet
from credenciais import CREDENTIALS

gn = Gerencianet(CREDENTIALS)

headers = {
    'x-skip-mtls-checking': 'false'
}

params = {
    'chave': '44ee453e-c14d-40c5-b7fd-8cca0bf55c70'
}

body = {
    'webhookUrl': 'https://mijaozinho.000.pe/' 
}

response =  gn.pix_config_webhook(params=params, body=body, headers=headers)
print(response)