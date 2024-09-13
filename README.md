# Gestão De Projeto

Links:
- RestFul API: http://127.0.0.1:8000/swagger/
- Graphql API: http://127.0.0.1:8000/api/graphql/

## Como iniciar o projeto

O projeto pode ser iniciado de duas formas:
1. Usando o `docker` 
2. Usando comando padrão do django

### 1. Usando o docker

Para iniciar o projeto voce precisa fazer alguns passos:
1. Criar um arquivo `.env` no root da aplicação
2. Copiar o conteudo de `contrib/env_example.txt`. 
3. Ao ter um arquivo `.env` com as credencias do banco de dados rode o seguinte comando:
```bash
docker compose up --build
```
A aplicação ira rodar na porta `8000`

### 2. Usando Comando Padrão Do Django

Caso voce queira usar o comando padrão do django voce terá que seguir alguns passos:
1. Crie e ative um ambiente virtual
`python3 -m venv venv && source venv/bin/activate`

2. Ao criar e ativar o ambiente, e necessario instalar os pacotes.
`pip install -r requirements.txt`

3. Ao instalar as dependencias voce estara pronto para rodar o projeto usando o comando padrao do django.
`python manage.py runserver`

## Funcionalidades
Foram criados dois tipos de `API Restful` com `rest_framework` e `Graphql API` usando o django-graphene.

No `API Restful` os endpoints CRUD from criados para os tres models (Cliente, Projeto e Atividade). Onde e usado requisições HTTP (GET, PUT, UPDATE e DELETE).

Endpoint para requisições da `API Restful` (documentação com requisições):
http://127.0.0.1:8000/swagger/

Ja para o `Graphql API` é usado apenas uma url para ser feito todo o CRUD dos tres models (Cliente, Projeto e Atividade). Baseado em um esquema que define tipos e campos. Oferece flexibilidade para consultas e manipulação de dados complexos. (não necessitando criar endpoints complexos na API Restful) reduzindo assim a manutenção do código.

Endpoint para queries e mutations da `Graphql API` (documetação com requisições):
http://127.0.0.1:8000/api/graphql/

## Test Unitários 

Para os testes unitários foram feitas apenas para as funcionalidades que foram criadas na aplicação. 

Neste caso, foi testado toda funcionalidade da API Restful e todas funcionalidades da API Graphql.
Voce pode conferi-los em `core/tests/`

### Coverage

Mais ainda, foi adicionado o coverage onde em `.coveragerc` foi setado quais arquivos deveriam ser testados no qual os seguintes foram adicionados:
- `*/models.py, */viewsets.py, */serializers.py, */queries.py, */mutations.py`

Além do mais a aplicação, usando o docker retorna o seguinte status:
```bash
 Name                        Stmts   Miss  Cover
 -----------------------------------------------
 core/api/serializers.py        14      0   100%
 core/api/viewsets.py           12      0   100%
 core/graphql/mutations.py     103      6    94%
 core/graphql/queries.py        48     18    62%
 core/models.py                 24      3    88%
 -----------------------------------------------
 TOTAL                         201     27    87% 
```
