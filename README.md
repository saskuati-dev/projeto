# Projeto de Software Sistema de Inscrições e Acompanhamento Desportivo (SIAD)

Este é um projeto Django produzido para a matéria de projeto de software do cuso de Eng. de Computação, para gerenciar eventos esportivos, incluindo modalidades, divisões, grupos, e atletas. O projeto também permite a administração de notícias e editais relacionados aos eventos.

## Funcionalidades

- **Gestão de Eventos**: Criação e administração de eventos esportivos.
- **Gestão de Grupos e Modalidades**: Adição e exclusão de grupos e modalidades para cada evento.
- **Gestão de Divisões**: Adição e exclusão de divisões para cada modalidade.
- **Notícias**: Adicione e visualize notícias relacionadas aos eventos.
- **Editais**: Upload e visualização de editais para cada evento.
- **Sistema de Login**: Autenticação e autorização para diferentes tipos de usuários (administradores e representantes esportivos).

## Tecnologias

- **Django**: Framework web para o desenvolvimento do projeto.
- **SQLite**: Banco de dados padrão para desenvolvimento.

## Instalação

### Requisitos

- Python 3.x
- pip (gerenciador de pacotes do Python)

### Passos para Instalação

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/saskuati-dev/projeto.git
   cd SIAD

   
2. **Instale as Dependências**

   ```bash
   pip install -r requirements.txt


3. **Crie um Superusuário**
   ```bash
   python manage.py createsuperuser

4. **Configure o Banco de Dados**
    ```bash
   python manage.py migrate

5. **Inicie o Servidor**
   ```bash
   python manage.py runserver

7.**Navegue até a aplicação**
  Navegue até http://127.0.0.1:8000/ para ver a aplicação em funcionamento




## Uso

### Acesso à Área Administrativa

Acesse a área administrativa em [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) usando as credenciais do superusuário que você criou durante a configuração inicial do projeto.

### Recursos Disponíveis

- **Eventos:** Crie, edite e visualize eventos esportivos.
- **Grupos e Modalidades:** Adicione e administre grupos e modalidades dentro dos eventos.
- **Divisões:** Gerencie divisões para modalidades.
- **Notícias:** Publique e visualize notícias.
- **Editais:** Faça upload e gerencie editais de eventos.

### Regras de Acesso

- **Administrador Esportivo:** Tem acesso completo à administração de eventos, grupos, modalidades, divisões, notícias e editais.
- **Representante Esportivo:** Pode acessar e gerenciar suas próprias inscrições e visualizar eventos e editais.

## Desenvolvimento

### Estrutura do Projeto

- **`app_siad/`**: Contém os modelos, formulários e visualizações da aplicação.
- **`templates/`**: Contém os templates HTML usados para renderizar as páginas.
- **`static/`**: Contém arquivos estáticos, como CSS e JavaScript.
- **`media/`**: Contém arquivos de mídia carregados pelo usuário, como imagens e documentos.


  
