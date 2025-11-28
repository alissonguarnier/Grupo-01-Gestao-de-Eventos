
# 📘 Sistema de Gestão de Eventos

## Estrutura do Sistema

### **Entidades**

### **Evento (A)**

Campos:

* `id`
* `nome`
* `descricao`
* `data_inicio`
* `data_fim`
* `local`

---

### **Atividade (B)**

Campos:

* `id`
* `titulo`
* `descricao`
* `horario_inicio`
* `horario_fim`
* `tipo`
* `evento_id`
* `responsavel_id`

---

### **Participante (C)**

Campos:

* `id`
* `nome`
* `email`
* `celular`
* `tipo`

---

## Relacionamentos

* **Evento (A) ↔ Atividade (B)** → **1:N**
* **Evento (A) ↔ Participante (C)** → **N:N**
* **Atividade (B) ↔ Participante (C)** → **1:1** ou **1:N**

### Diagrama textual

```
Evento (1) ──── (N) Atividade ──── (1) Participante (responsável)
     │
     └─── (N:N) Participante (inscritos)
```

---

## Regras de Permissão

### **Admin/Staff**

* Criar, editar e excluir eventos, atividades e participantes.
* Definir responsável da atividade.

### **Participante Autenticado**

* Visualizar seus dados, eventos e atividades.

### **Usuário Anônimo**

* Listar eventos e atividades.

---

# Rotas da API

## **Eventos (A)**

| Método    | Rota                 | Função   |
| --------- | -------------------- | -------- |
| GET       | `/api/eventos/`      | Listar   |
| POST      | `/api/eventos/`      | Criar    |
| GET       | `/api/eventos/{id}/` | Detalhar |
| PUT/PATCH | `/api/eventos/{id}/` | Editar   |
| DELETE    | `/api/eventos/{id}/` | Excluir  |

**Relacionamentos**

```
GET /api/eventos/{id}/participantes/
POST /api/eventos/{id}/participantes/

GET /api/eventos/{id}/atividades/
POST /api/eventos/{id}/atividades/

GET /api/eventos/{id}/dashboard/
```

---

## **Participantes (C)**

| Método    | Rota                       | Função   |
| --------- | -------------------------- | -------- |
| GET       | `/api/participantes/`      | Listar   |
| POST      | `/api/participantes/`      | Criar    |
| GET       | `/api/participantes/{id}/` | Detalhar |
| PUT/PATCH | `/api/participantes/{id}/` | Editar   |
| DELETE    | `/api/participantes/{id}/` | Excluir  |

---

## **Atividades (B)**

| Método    | Rota                    | Função   |
| --------- | ----------------------- | -------- |
| GET       | `/api/atividades/`      | Listar   |
| POST      | `/api/atividades/`      | Criar    |
| GET       | `/api/atividades/{id}/` | Detalhar |
| PUT/PATCH | `/api/atividades/{id}/` | Editar   |
| DELETE    | `/api/atividades/{id}/` | Excluir  |

**Responsável**

```
GET /api/atividades/{id}/responsavel/
POST /api/atividades/{id}/responsavel/
```

---

# Rotas de Relacionamento

### **A ↔ C**

```
GET /api/eventos/{id}/participantes/
POST /api/eventos/{id}/participantes/
```

### **A ↔ B**

```
GET /api/eventos/{id}/atividades/
POST /api/eventos/{id}/atividades/
```

### **B ↔ C**

```
GET /api/atividades/{id}/responsavel/
POST /api/atividades/{id}/responsavel/
```

---

# Rota Cruzada A-B-C

```
GET /api/eventos/{id}/dashboard/
```

---

# Rotas Gerais

| Rota               | Função       |
| ------------------ | ------------ |
| `/api/`            | Raiz         |
| `/api/auth/token/` | Autenticação |
| `/api/schema/`     | OpenAPI      |
| `/api/docs/`       | Swagger      |
| `/api/docs/redoc/` | ReDoc        |

---

## Fluxo de Operação

1. Criar Evento
2. Criar Atividades
3. Criar Participantes
4. Inscrever participantes
5. Definir responsáveis
6. Consultar eventos e atividades
7. Usar dashboard


