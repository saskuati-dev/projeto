from gerencianet import Gerencianet
from credenciais import CREDENTIALS

gn = Gerencianet(CREDENTIALS)

response =  gn.pix_create_evp()
print(response)