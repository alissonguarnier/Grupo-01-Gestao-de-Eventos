# Enunciado do Projeto – Sistema de Gestão de Projetos Colaborativos (DevLab

## **Contexto**

O DevLab é um programa de uma instituição de ensino que reúne turmas de cursos técnicos e superiores em Computação para desenvolver projetos reais para clientes internos (professores, setores administrativos, coordenações) e externos (comunidade, empresas parceiras).

Atualmente, o coordenador utiliza planilhas, grupos de WhatsApp e documentos soltos para gerenciar os projetos, equipes e participantes, o que gera desorganização e falta de controle.

O objetivo é criar um sistema web interno, com backend em Python/Django, para centralizar a gestão de projetos, equipes e usuários, permitindo autenticação e controle de acesso diferenciado por perfil.

## **Objetivos**

Implementar uma API REST que permita:

- Coordenadores/Administradores gerenciarem projetos, equipes e usuários.
- Usuários comuns (estudantes/professores) consultarem apenas os projetos e equipes em que participam.
- Definir líderes de equipe (cada equipe tem um único líder).
- Um usuário pode ser líder de apenas uma equipe.
- Permitir que usuários participem de vários projetos e equipes.
- Gerar relatórios e visões agregadas sobre participação dos usuários.

## **Estrutura de Dados**

O sistema pode conter 3 entidades principais (sugestão):

- **User** – modelo padrão do Django para autenticação.
- **Projeto** – cadastro de projetos do DevLab.
- **Equipe** – equipes vinculadas a projetos, com membros e líder.

Relacionamentos:

- N:N entre User ↔ Projeto (um usuário participa de vários projetos e um projeto tem vários usuários).
- 1:N entre Projeto ↔ Equipe (um projeto pode ter várias equipes).
- 1:1 entre User ↔ Equipe (liderança: cada equipe tem um líder, e cada usuário pode liderar no máximo uma equipe).

**Escopo (o que o sistema precisa fazer)**

**Funcionalidades mínimas**

- **Autenticação**
  - Usuário deve conseguir fazer login.
  - Algumas rotas devem ser protegidas (só acessíveis para usuário autenticado).
  - Diferenciar pelo menos dois perfis:
  - Administrador/Coordenador: pode gerenciar todos os dados.
  - Usuário comum (estudante/professor): tem acesso limitado (ex.: ver projetos em que participa).

- **Gestão de Projetos**
  - CRUD completo de projetos:
  - Criar, listar, buscar por ID, atualizar, remover.
  - Atributos sugeridos:
  - titulo, descricao, cliente, status (planejado, em andamento, concluído), data_inicio, data_fim_prevista.

- **Gestão de Equipes**
  - Cada projeto pode ter várias equipes.
  - Cada equipe pertence a um único projeto.
  - CRUD completo de equipes.
  - Atributos sugeridos:
  - nome, descricao, projeto, lider (um usuário responsável pela equipe – relacionamento 1:1 entre usuário e liderança de equipe; um usuário pode ser líder de no máximo uma equipe).
  - Gestão de Usuários / Participação
  - Criar um modelo de domínio (ex.: Perfil ou Participante) associado ao Usuário se quiser guardar dados extras (curso, matrícula, tipo de usuário etc.).
  - Cada usuário pode participar de vários projetos, e cada projeto pode ter vários usuários → relacionamento N:N.
  - Uma equipe é formada por vários usuários, mas tem um líder (o líder também é um usuário participante).

**Principais usuários e atores**

- **Coordenador DevLab (Administrador)**
  - Ator com maior privilégio.
  - Cadastra e gerencia projetos.
  - Cria e edita equipes.
  - Associa usuários a projetos.
  - Define líderes de equipe.
  - Visualiza relatórios gerais (quem participa de quê).

- **Professor/Mentor**
  - Pode consultar os projetos e equipes.
  - Pode ver quais estudantes participam de cada projeto.
  - Pode consultar as equipes sob sua responsabilidade (opcional, conforme você modelar).

- **Estudante**
  - Participa de projetos e equipes.
  - Pode ver os projetos em que está cadastrado.
  - Pode ver sua equipe, líder e colegas.
  - Opcionalmente, pode editar alguns dados próprios (ex.: perfil, curso).

- **Usuário não autenticado (visitante)**
  - Pode ter acesso apenas a rotas públicas (por exemplo, listagem simplificada de projetos sem dados sensíveis) — opcional, definido por você.

## **Requisitos Mínimos**

- CRUD completo para cada entidade (User, Projeto, Equipe).
- **No mínimo 3 rotas de relacionamento:**
  - Usuário ↔ Projeto (A-B).
  - Projeto ↔ Equipe (B-C).
  - Usuário ↔ Projeto ↔ Equipe (A-B-C).
- **Autenticação: login via Django Auth.**
- **Controle de acesso por perfil:**
  - Coordenadores/Admins → CRUD completo em todas as entidades.
  - Usuários comuns → apenas consultas de seus projetos e equipes.
- Registro no admin: todas as tabelas devem estar disponíveis.
- Documentação da API: pode ser gerada com drf-spectacular.

## **Sugestão de Modelagem**

### **Entidade: User (já existe no Django, não deve ser alterada)**

- Campos principais:
  - id (PK)
  - username
  - email
  - password
  - is_active, is_staff, is_superuser
- Relacionamentos:
  - N:N com Projeto (participação).
  - 1:1 com Equipe (quando atua como líder).

### **Entidade: Projeto**

- Campos principais:
  - id (PK)
  - titulo
  - descricao
  - cliente
  - status (planejado, em andamento, concluído)
  - data_inicio
  - data_fim_prevista
- Relacionamentos:
  - N:N com User (participantes).
  - 1:N com Equipe.

### **Entidade: Equipe**

- Campos principais:
  - id (PK)
  - nome
  - descricao
  - projeto_id (FK → Projeto)
  - lider_id (FK → User, relacionamento 1:1)
- Relacionamentos:
  - 1:N com Projeto.
  - N:N com User (membros).
  - 1:1 com User (liderança).

## **Sugestão de Rotas da API**

### **Rota principal**

- /api/ → ponto de entrada da API (pode listar recursos disponíveis ou redirecionar para documentação).

### **Usuários**

- /api/users/ → CRUD de usuários (apenas coordenadores/admins).
- /api/users/{id}/projetos/ → listar projetos em que o usuário participa.
- /api/users/{id}/equipes/ → listar equipes em que o usuário participa.
- /api/users/{id}/visao-geral/ → visão geral: dados do usuário, projetos e equipes relacionadas.

### **Projetos**

- /api/projetos/ → CRUD de projetos (coordenadores/admins).
- /api/projetos/{id}/equipes/ → listar equipes de um projeto.
- /api/projetos/{id}/participantes/ → adicionar usuário ao projeto.
- /api/projetos/{id}/dashboard/ → visão geral do projeto com equipes e membros.

### **Equipes**

- /api/equipes/ → CRUD de equipes (coordenadores/admins).
- /api/equipes/{id}/definir-lider/ → definir usuário como líder da equipe.

### **Autenticação**

- /api/auth/login/ → login via Django Auth.
- /api/auth/token/ → obtenção de token (DRF Token Authentication).

### **Documentação**

- /api/schema/ → schema OpenAPI.
- /api/docs/ → documentação interativa.
- /api/docs/redoc/ → documentação interativa.

## **Sugestão de Melhorias**

- Implementação de relatórios agregados (quantos projetos cada aluno participou, em quais equipes e funções).
- Implementação de filtros avançados (django-filter).
- Possibilidade de rotas públicas para listagem simplificada de projetos (sem dados sensíveis).
- Diagrama ER e casos de uso para melhor visualização dos relacionamentos.

**Entregáveis**

**Os alunos devem entregar:**

- **Código-fonte**
  - Todo o código-fonte estará no GitHub. Você pode utilizar este template como modelo - https://github.com/claulis/templateBFD
  - Modelos, views, URLs e (se usarem DRF) serializers organizados.
  - Arquivo de requisitos.

**Documentação de software**

- README com:
  - Descrição do sistema.
  - Como instalar dependências.
  - Como configurar o banco.
  - Como criar usuário admin.
  - Como rodar o servidor e testar a API.

- **Documentação da API:**
  - Lista de endpoints com:
  - método HTTP, URL, parâmetros,
  - exemplo de request/response.
  - Pode ser em Markdown, tabela ou via Swagger/OpenAPI/redoc se quiserem.

**Descrição do modelo de dados:**

- Diagrama ER ou explicação textual das entidades e relacionamentos (indicando 1:1, 1:N, N:N). MER com a descrição do banco de dados.
- (Opcional) Diagrama de casos de uso, mostrando as ações de cada ator (coordenador, professor, estudante).

**Link da Publicação da Aplicação (opcional, mas recomendado).**