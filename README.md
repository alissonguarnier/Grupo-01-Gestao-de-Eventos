# 📘 EventLab API — Sistema de Gestão de Eventos

# 📑 Sumário

1. Visão Geral
2. Pacotes Utilizados
3. Estrutura do Projeto
4. Diagrama de Banco de Dados
5. Documentação da API
6. Configuração do Ambiente
7. Deploy

---

# 🎯 Visão Geral

A **EventLab API** é um sistema backend para **gestão de eventos**, permitindo organizar:

* **Eventos (A)**
* **Atividades (B)**
* **Participantes (C)**

O sistema utiliza autenticação, permissões de acesso e rotas de relacionamento entre entidades.

### Permissões

**Admin/staff**

* Criar, editar e excluir eventos e atividades
* Cadastrar participantes
* Definir responsáveis por atividades

**Participante autenticado**

* Consultar seus dados pessoais
* Visualizar eventos e atividades

**Usuário anônimo**

* Visualizar apenas eventos e atividades públicas

### Funcionalidades Principais

* CRUD completo de **Eventos, Atividades e Participantes**
* Inscrição de participantes em eventos
* Definição de responsáveis pelas atividades
* Relacionamentos entre Evento ↔ Atividade ↔ Participante
* Dashboard geral do evento (A-B-C)
* Documentação interativa da API via Swagger e ReDoc

---

# 📦 Pacotes Utilizados

| Pacote                   | Versão | Descrição              |
| ------------------------ | ------ | ---------------------- |
| Django                   | ≥5.0   | Framework principal    |
| django-filter            | latest | Função filter do django|
| djangorestframework      | latest | API REST               |
| drf-spectacular          | latest | Documentação OpenAPI   |
| drf-spectacular-sidecar  | latest | UI Swagger/ReDoc       |
| django-cors-headers      | latest | Segurança do HTML      |

> A lista completa e as versões exatas estão em **requirements.txt**.

---

# 📁 Estrutura do Projeto

```
GRUPO-01-GESTAO-DE-EVENTOS/
├── manage.py
├── requirements.txt
├── README.md
├── projeto/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── gestaoEventos/
│   ├── management/
│   │   ├── commands/
│   │   │   ├── importar_dados
│   │   │   ├── ...
│   │   └── ...
│   ├── migrations/
│   │   ├── initial.py
│   │   ├── alter_usereventos_options.py
│   │   └── ...
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
└── docs/
    ├── management/
    │   ├── DER_banco.pu
    │   └── MER_banco.brM3
    ├── 01-Enunciado.md
    ├── 02-Documentacao-extra.md
    ├── 03-DER_banco.png
    └── 04-MER_banco.png

```

* **projeto/** → Configurações principais do Django
* **gestaoEventos/** → Aplicação principal (modelos, views, serializers, routers)
* **docs/** → Diagramas e arquivos de documentação

---

# 🗂️ Diagrama de Banco de Dados

## Entidades e Relacionamentos

![DER_banco](docs/03-DER_Banco.png)


### **Evento (A)**

| Campo       | Tipo      | Descrição               |
| ----------- | --------- | ----------------------- |
| id          | PK        | Identificador do evento |
| nome        | CharField | Nome do evento          |
| descricao   | TextField | Descrição               |
| data_inicio | DateField | Data de início          |
| data_fim    | DateField | Data de término         |
| local       | CharField | Localização             |

---

### **Atividade (B)**

| Campo          | Tipo          | Descrição                       |
| -------------- | ------------- | ------------------------------- |
| id             | PK            | Identificador da atividade      |
| titulo         | CharField     | Nome da atividade               |
| descricao      | TextField     | Descrição                       |
| horario_inicio | DateTimeField | Início                          |
| horario_fim    | DateTimeField | Fim                             |
| tipo           | CharField     | Tipo (palestra, oficina…)       |
| evento_id      | FK            | Relacionamento com Evento       |
| responsavel_id | FK            | Relacionamento com Participante |

---

### **Participante "User" (C)**

| Campo   | Tipo       | Descrição                               |
| ------- | ---------- | --------------------------------------- |
| id      | PK         | Identificador                           |
| nome    | CharField  | Nome completo                           |
| email   | EmailField | Email                                   |
| celular | CharField  | Telefone                                |
| tipo    | CharField  | Perfil (aluno, palestrante, convidado…) |

### **UserEvento "Inscrição" (D)**

| Campo        | Tipo       | Descrição                               |
| ------------ | ---------- | --------------------------------------- |
| id           | PK         | Identificador                           |
| user_id      | FK         | Relacionamento com user (participante)  |
| evento_id    | Fk         | Relacionamento com evento               |
|data_inscricao| CharField  | Telefone                                |


---

## 🔗 Relacionamentos

* **Evento (1) → (N) Atividade**
* **Evento (N) ↔ (N) Participante (User)**
* **Atividade (1) → (1) Participante (responsável)**

### 📐 Representação Textual

```
Evento (1) ─── (N) Atividade ─── (1) Participante (responsável)
     │
     └── (N:N) Participante (inscritos)
```

---

# 📚 Documentação da API

A documentação interativa está disponível em:

* **/api/docs/** → Swagger UI
* **/api/docs/redoc/** → ReDoc
* **/api/schema/** → Arquivo OpenAPI

---

# 🔍 Endpoints Principais

| Método | Endpoint                            | Descrição                         | Auth        |
| ------ | ----------------------------------- | --------------------------------- | ----------- |
| GET    | `/api/eventos/`                     | Lista todos os eventos            | Opcional    |
| GET    | `/api/eventos/{id}/dashboard/`      | Detalhes completos do evento      | Autenticada |
| GET    | `/api/atividades/`                  | Lista atividades                  | Opcional    |
| POST   | `/api/atividades/{id}/responsavel/` | Define responsável pela atividade | Admin       |
| GET    | `/api/participantes/{id}/`          | Detalhes do participante          | Autenticada |
| GET    | `/api/eventos/{id}/participantes/`  | Lista de inscritos no evento      | Autenticada |

---

# ⚙️ Configuração do Ambiente

### 1. Clonar o repositório

```
git clone https://github.com/usuario/eventlab.git
cd eventlab
```

---

### 2. Criar o ambiente virtual

**Linux/Mac:**

```
python -m venv venv
source venv/bin/activate
```

**Windows:**

```
venv\Scripts\activate
```

---

### 3. Instalar dependências

```
pip install -r requirements.txt
```

---

### 4. Configurar variáveis de ambiente

```
cp .env.example .env
```

---

### 5. Executar migrações e iniciar o servidor

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

# 🚀 Deploy (Opcional)

**Plataformas recomendadas:** Render · Railway · AWS

### Procfile

```
web: gunicorn config.wsgi:application --log-file -
```

### Comandos adicionais

```
python manage.py migrate
python manage.py collectstatic
```

