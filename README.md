# rota-rota-jequiti: projeto de pastejo rotacionado

<img src="frontend/img/perfil.jpg" alt="Logo do projeto" align="left" width="180" hspace="16" />

Trabalho 03 de Desenvolvimento Web III

Sistema web para controle de **pastejo rotacionado** (módulo agrícola de um ERP). Permite cadastrar **Pastos**, **Piquetes**, **Animais** e **Alocações** (qual animal está em qual piquete e por quanto tempo), com login e rotas protegidas por JWT.

<br clear="left" />

<br>

| Camada | Tecnologia | Porta |
| --- | --- | --- |
| Front-end | Node.js + Express (HTML/CSS/JS puro) | 3000 |
| Back-end (API REST) | Python + Flask | 5000 |
| Banco de dados | PostgreSQL 16 | 5431 (host) |

## Como executar

Pré-requisito: Docker Desktop aberto.

```
docker compose up --build -d
```

Acesse http://localhost:3000
- login `dw3`
- senha `dw3`

Zerar o banco: `docker compose down -v && docker compose up --build -d`

## Diagrama Entidade Relacionamento (DER)

```mermaid
erDiagram
    PASTO ||--o{ PIQUETE : "possui (1:N)"
    PIQUETE ||--o{ ALOCADO : "recebe (1:N)"
    ANIMAL ||--o{ ALOCADO : "é alocado em (1:N)"

    USUARIO {
        serial usuarioid PK
        varchar(50) login UK
        varchar(100) senha "hash bcrypt"
        boolean removido
    }

    PASTO {
        serial pastoid PK
        varchar(100) descricao
        numeric(10,2) areatotal
        boolean removido
    }

    PIQUETE {
        serial piqueteid PK
        varchar(100) descricao
        numeric(10,7) latitude
        numeric(10,7) longitude
        integer pastoidfk FK
        boolean removido
    }

    ANIMAL {
        serial animalid PK
        varchar(100) nome
        date datanasc
        boolean removido
    }

    ALOCADO {
        serial alocadoid PK
        integer animalidifk FK
        integer piqueteidfk FK
        date datainicio
        date datafinal "opcional"
        boolean removido
    }
```

- **Pasto → Piquete (1:N):** um pasto tem vários piquetes; cada piquete pertence a um pasto.
- **Piquete → Alocado (1:N)** e **Animal → Alocado (1:N):** cada alocação liga um animal a um piquete.
- **Animal ↔ Piquete (N:N):** um animal passa por vários piquetes e um piquete recebe vários animais. A tabela **ALOCADO** resolve essa relação e registra o período (`datafinal` vazia = ainda está no piquete).
- **USUARIO** serve só para o login e não se relaciona com as demais.

---

## Observações

- **Senha com hash (bcrypt):** a senha não é guardada em texto puro. `dw3` vira um hash de 60 caracteres (`$2a$06$...`), gerado no banco (`crypt('dw3', gen_salt('bf'))`, em `database/init.sql`) e conferido no login com `bcrypt.checkpw`.
- O hash muda a cada criação do banco (o sal é aleatório), por isso o valor não está escrito aqui.
- **Token:** a API devolve um **JWT válido por 1 hora**. Sem token válido, as rotas respondem `401` e o front volta para o login.
- **Exclusão lógica:** excluir só marca `removido = true`, e nada é apagado do banco.
- As exclusões não são em cascata: apagar um pasto, piquete ou animal não remove os registros ligados a ele.
- O sistema não impede que um animal tenha duas alocações com períodos sobrepostos.
- Senha do banco e `JWT_SECRET` ficam no arquivo `.env`, que não vai para o GitHub. O `.env.example` mostra quais variáveis são necessárias.

## Estrutura

```
backend/apps/<modulo>/controller + model   (pasto, piquete, animal, alocado, login)
frontend/apps/<modulo>/vw<Modulo>.js       (+ apps/shared: auth, api, crud, layout)
database/init.sql
```