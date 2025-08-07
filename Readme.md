# Projeto de requisições de atendimento


## Sobre o projeto
Este projeto foi desenvolvido para gerenciar e agendar atendimentos online para a equipe de suporte e tecnologia da cidade e municipios de Monte Alegre.

Sistema por: @Hetrisley_Gomes.

## Estrtutura de Pastas
```
/src                    # Código-fonte principal da aplicação
    /controllers        # Funções de controle de rotas
    /models             # Modelos de dados SQLite
        /repositories   # Gerencia os dados do banco de dados
        /settings       # Estabelece conexão com o banco de dados
    /main               # Componentes principais da aplicação
        /routes         # Definição de rotas da API
        /server         # Configura o servidor Flask e a conexão de Socket
        /static         # Arquivos estáticos, como imagens e folhas de estilo
        /templates      # Documentos html
/init                   # Inicializa o servidor Flask e a conexão com o banco de dados
```

## Tecnologias Usadas
- **venv**: Uma ferramenta integrada no Python para criar ambientes virtuais isolados, permitindo a instalação de dependências específicas do projeto sem interferir no sistema global.

- **Flask**: Um micro framework para Python que facilita o desenvolvimento de aplicações web rápidas e escaláveis com simplicidade e flexibilidade.

- **jQuery**: Uma biblioteca JavaScript que simplifica a manipulação do DOM, o tratamento de eventos e as chamadas Ajax, melhorando a compatibilidade entre navegadores.

- **Ajax**: Uma técnica para atualizar partes de uma página web de forma assíncrona sem recarregar a página inteira, proporcionando uma experiência de usuário mais dinâmica e interativa.

- **SQLite**: Um banco de dados relacional leve e autônomo que armazena dados em um único arquivo, ideal para aplicações de pequeno a médio porte e desenvolvimento rápido.

- **Bootstrap**: Um framework front-end que fornece um conjunto de ferramentas e componentes responsivos para criar layouts e design web consistentes e modernos

## Rodando Localmente
Clone do repositório:
```bash
git clone https://github.com/HetrisleyGomes/projeto-equipe-tecnologia.git
```


Instalando dependências:
```bash
pip install -r requirements.txt
```

Inicializando o ambiente virtual:
```bash
. .\.venv\Scripts\activate
```

Inicializando o servidor:
```bash
py run.py
```

## Funcionalidades
- **Listar requisições**: Retorna todas as reuisições do banco de dados, podendo aplicar filtros de busca.
- **Criar requisições**: Permite que qualquer usuáruio na rede crie uma nova requisição.
- **Atualizar requisições**: Permite que os membros da equipe de tecnologia atualize os dados de uma requisição.
- **Finalizar requisições**: Oculta requisições concluídas da lista de busca.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
