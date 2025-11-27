# Sistema de Projetos, Equipes e Usuários

## Estrutura do Sistema

### **Entidades**
- **User (C)**
  - Modelo padrão do Django (`auth_user`).
  - Pode estar em várias equipes.
  - Pode liderar uma equipe (ou nenhuma).

- **Projeto (A)**
  - Agrupa várias equipes.
  - Participantes são derivados dos membros das equipes.

- **Equipe (B)**
  - Pertence a um único projeto.
  - Tem vários membros (Users).
  - Tem um líder (User), que também deve estar cadastrado como membro.

---

##  Relacionamentos

- **Projeto (A) ↔ Equipe (B)** → **1:N**
- **Equipe (B) ↔ User (C)** → **N:N** (membros)
- **Equipe (B) ↔ User (C)** → **1:1** (líder)

### Diagrama textual

```
Projeto (1) ──── (N) Equipe ──── (N) User (membros)
                          │
                          └─── (1) User (líder)
```

### **Projeto ↔ Equipe**

- **1:N (um para muitos)**
  - Um **Projeto** pode ter várias **Equipes**.
  - Cada **Equipe** pertence a **um único Projeto**.
  - Implementado com `ForeignKey` em `Equipe` apontando para `Projeto`.

### **Equipe ↔ User (membros)**

- **N:N (muitos para muitos)**
  - Uma **Equipe** pode ter vários **Users** como membros.
  - Um **User** pode participar de várias **Equipes**.
  - Implementado com `ManyToManyField` em `Equipe` apontando para `User`.

### **Equipe ↔ User (líder)**

- **1:1 (um para um)**
  - Uma **Equipe** tem **um único líder**.
  - Um **User** pode liderar **apenas uma equipe** (ou nenhuma).
  - Implementado com `OneToOneField` em `Equipe` apontando para `User`.

## Interpretação prática

- **Projeto**: agrupa várias equipes.

- **Equipe**: pertence a um projeto, tem vários membros e um líder.

- **User**: pode estar em várias equipes e pode ser líder de uma delas.

- **Participantes do projeto**: não são armazenados diretamente, mas calculados a partir dos membros das equipes vinculadas.

  

---

## Regras de Permissão

- **Admin/staff**
  - Pode criar, editar e excluir projetos e equipes.
  - Pode definir líder da equipe.

- **Usuário comum (aluno/professor)**
  - Só pode **listar e consultar** projetos e equipes em que participa.
  - Não pode criar, editar ou excluir.
  - Tentativas de `PATCH`, `DELETE` ou `POST` retornam `403 Forbidden`.

---

## Rotas Principais

### 🔹 Users
- `GET /api/users/{id}/projetos/` → projetos em que o usuário participa.
- `GET /api/users/{id}/equipes/` → equipes em que o usuário está.
- `GET /api/users/{id}/visao_geral/` → visão geral (dados do usuário, projetos e equipes).

### 🔹 Projetos
- `GET /api/projetos/` → lista de projetos (admin vê todos, usuário comum só os seus).
- `GET /api/projetos/{id}/equipes/` → equipes do projeto.
- `GET /api/projetos/{id}/participantes/` → participantes do projeto (via equipes).
- `GET /api/projetos/{id}/dashboard/` → projeto + equipes + participantes.

### 🔹 Equipes
- `GET /api/equipes/` → lista de equipes (admin vê todas, usuário comum só as suas).

- `GET /api/equipes/{id}/` → detalhes da equipe (inclui membros e líder).

- `POST /api/equipes/{id}/definir_lider/` → define líder (apenas admin).

  

---

## Rotas de relacionamento

### A ↔ B (Projeto ↔ Equipes)

- **Listar equipes de um projeto**

  Código

  ```
  GET /api/projetos/{id}/equipes/
  ```

  → retorna todas as equipes vinculadas ao projeto.

- **Dashboard do projeto (com equipes e participantes)**

  ```
  GET /api/projetos/{id}/dashboard/
  ```

  → retorna dados do projeto, suas equipes e os participantes derivados.

### B ↔ C (Equipe ↔ Users)

- **Listar membros de uma equipe**

  ```
  GET /api/equipes/{id}/
  ```

  → já retorna os membros no serializer.

- **Definir líder da equipe (admin apenas)**

  ```
  POST /api/equipes/{id}/definir_lider/
  {
    "user_id": 2
  }
  ```

  → define o líder, desde que ele já esteja cadastrado como membro.

### A ↔ C (Projeto ↔ Users)

- **Listar participantes de um projeto**

  

  ```
  GET /api/projetos/{id}/participantes/
  ```

  → retorna todos os usuários que estão em equipes do projeto.

- **Projetos de um usuário**

  

  ```
  GET /api/users/{id}/projetos/
  ```

  → retorna todos os projetos em que o usuário participa (via equipes).

### A ↔ B ↔ C (Projeto ↔ Equipes ↔ Users)

- **Visão geral de um usuário**

  

  ```
  GET /api/users/{id}/visao_geral/
  ```

  → retorna dados do usuário, os projetos em que participa e as equipes em que está.

- **Dashboard do projeto**

  

  ```
  GET /api/projetos/{id}/dashboard/
  ```

  → retorna dados do projeto, suas equipes e todos os participantes (users).

## Resumindo

- **A-B** → `/api/projetos/{id}/equipes/`
- **B-C** → `/api/equipes/{id}/` (membros) e `/api/equipes/{id}/definir_lider/`
- **A-C** → `/api/projetos/{id}/participantes/` e `/api/users/{id}/projetos/`
- **A-B-C** → `/api/users/{id}/visao_geral/` e `/api/projetos/{id}/dashboard/`



# Rotas principais da API

| Rota               | Descrição                                                    |
| ------------------ | ------------------------------------------------------------ |
| `/api/`            | Endpoint raiz da API. Normalmente lista ou organiza os recursos disponíveis. |
| `/api/docs/`       | Documentação interativa gerada pelo **Swagger UI**/**spectacular**. Permite testar endpoints diretamente pelo navegador. |
| `/api/docs/redoc/` | Documentação alternativa gerada pelo **ReDoc**. Apresenta os endpoints de forma organizada e amigável para leitura. |



## Fluxo

1. **Criar Projeto** (admin).
2. **Criar Equipe** vinculada ao projeto (admin).
3. **Adicionar membros** à equipe (admin).
4. **Definir líder** da equipe (admin, e o líder deve estar nos membros).
5. **Consultar Projeto** → participantes aparecem automaticamente.
6. **Usuário comum** → só consegue listar/consultar suas equipes e projetos.

---

