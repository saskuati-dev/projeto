from gerencianet import Gerencianet
from credenciais import CREDENTIALS
import base64

gn = Gerencianet(CREDENTIALS)

body = {
    'calendario': {
        'expiracao': 600
    },
    'devedor': {
        'cpf': '13528915900',
        'nome': 'João Carneiro'
    },
    'valor': {
        'original': '0.01'
    },
    'chave': '44ee453e-c14d-40c5-b7fd-8cca0bf55c70',
    'solicitacaoPagador': 'Cobrançaa por cada atleta inscito.'
}

response =  gn.pix_create_immediate_charge(body=body)
params = {
    'id': response['loc']['id']
}

response =  gn.pix_generate_QRCode(params=params)
print(response)
print('---------------------------------------')

#Generate QRCode Image
if('imagemQrcode' in response):
    with open("qrCodeImage.png", "wb") as fh:
        fh.write(base64.b64decode(response['imagemQrcode'].replace('data:image/png;base64,', '')))