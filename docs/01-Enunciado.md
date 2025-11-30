# Enunciado do Projeto – Sistema de Gestão de Eventos

## **Contexto**

Grandes eventos como congressos, conferências, semanas acadêmicas e feiras precisam de organização estruturada para gerenciar suas atividades (palestras, workshops, oficinas) e os participantes inscritos.

Atualmente, muitos organizadores ainda dependem de planilhas e formulários soltos para controlar tudo, o que gera falhas, perda de informações e dificuldade de gestão.

O objetivo deste projeto é desenvolver uma API REST em Django que centralize e organize
a gestão de eventos, participantes e atividades, com autenticação e controle de acesso.

## **Objetivos**

Implementar um sistema backend que permita:

- Cadastrar e gerenciar eventos, participantes e atividades.
- Relacionar participantes a eventos e atividades.
- Definir responsáveis por atividades (palestrantes, facilitadores).
- Garantir segurança e organização dos dados com autenticação e permissões.
- Disponibilizar documentação clara da API para facilitar integração com outros
  sistemas.

## **Estrutura de Dados**

O sistema pode conter 3 entidades principais (sugestão):

- **Evento** – cadastro de eventos.
- **Participante** – cadastro de pessoas inscritas ou responsáveis.
- **Atividade** – cadastro de atividades dentro de um evento.

**Relacionamentos obrigatórios:**

- **1:N** Evento ↔ Atividade (um evento possui várias atividades).
- **N:N** Evento ↔ Participante (um participante pode se inscrever em vários eventos).
- **1:1** (ou 1:N) Atividade ↔ Participante (responsável pela atividade).

## **Requisitos Mínimos**

- Rotas de backend implementando métodos GET, POST, PUT, DELETE.
- CRUD completo para cada entidade.
- No mínimo 3 rotas de relacionamento:
  - Evento ↔ Participante (N:N).
  - Evento ↔ Atividade (1:N).
  - Atividade ↔ Participante (1:1).
- Uma rota composta cruzando as três entidades (Evento ↔ Participante ↔
  Atividade).
- Autenticação:
  - Rotas restritas para criação/edição/exclusão de eventos e atividades.
  - Rotas públicas para listagem de eventos e atividades.
- Registro no admin: todas as tabelas devem estar disponíveis.
- Documentação da API: gerada com Swagger/OpenAPI.

## **Sugestão de Modelagem**

### **Entidade: Evento**

Campos principais:

- id (PK)
- nome
- descricao
- data_inicio
- data_fim
- local

Relacionamentos:

- 1:N com Atividade
- N:N com Participante

### **Entidade: Participante (user?)**

Campos principais:

- id (PK)
- nome
- email
- celular
- tipo (estudante, convidado, palestrante etc.)

Relacionamentos:

- N:N com Evento
- 1:1 (ou 1:N) com Atividade (como responsável)

### **Entidade: Atividade**

Campos principais:

- id (PK)
- titulo
- descricao
- horario_inicio
- horario_fim
- tipo (workshop, palestra, oficina etc.)
- evento_id (FK → Evento)
- responsavel_id (FK → Participante)

Relacionamentos:

- 1:N com Evento
- 1:1 (ou 1:N) com Participante (responsável)


Sugestão do professor:

Entidade:
- Perfil (completar o users)
- Atividade
- Evento

-Criar dois grupos no views: 
  - Participantes
  - Organizadores

## **Sugestão de Rotas da API**

### **Rota principal**

- /api/ → ponto de entrada da API.

### **Eventos**

- /api/eventos/ → CRUD de eventos.
- /api/eventos/{id}/ → detalhes de um evento.
- /api/eventos/{id}/participantes/ → listar ou inscrever participantes em
  um evento.
- /api/eventos/{id}/atividades/ → listar ou cadastrar atividades de um
  evento.
- /api/eventos/{id}/dashboard/ → visão completa do evento (atividades,
  responsáveis, participantes).

### **Participantes**

- /api/participantes/ → CRUD de participantes.
- /api/participantes/{id}/ → detalhes de um participante.

### **Atividades**

- /api/atividades/ → CRUD de atividades.
- /api/atividades/{id}/ → detalhes de uma atividade.
- /api/atividades/{id}/responsavel/ → definir ou consultar responsável da
  atividade.

### **Autenticação**

- /api/auth/token/ → obtenção de token.

### **Documentação**

- /api/schema/ → schema OpenAPI.
- /api/docs/ → documentação interativa.
- /api/docs/redoc/ → documentação interativa.

## **Sugestão de Melhorias**

- Implementação de relatórios de participação por evento.
- Implementação de filtros avançados (ex.: por tipo de atividade, por perfil de
  participante).
- Dashboard com estatísticas de eventos e atividades.

**Entregáveis**

- Código fonte.
- Repositório GitHub organizado.
- Modelos, rotas, controllers/services.
- Arquivo de dependências (requirements.txt).
- Scripts de migração.
- Estrutura de pastas limpa.
- Documentação:
  - README com instruções de instalação e uso.
  - Documentação da API (Swagger/OpenAPI).
  - Modelo de dados (MER + DER).
  - Diagrama de casos de uso (opcional).
