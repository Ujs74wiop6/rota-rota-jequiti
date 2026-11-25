# rota-rota-jequiti: projeto de pastejo rotacionado

Trabalho 03 de Desenvolvimento Web III

CRUD de **Pasto**, **Piquete**, **Animal** e **Alocado** (módulo agrícola de pastejo rotacionado), com login e JWT.

| Camada | Tecnologia | Porta |
| --- | --- | --- |
| Front-end | Node.js + Express (HTML/CSS/JS puro) | 3000 |
| Back-end (API REST) | Python + Flask | 5000 |
| Banco de dados | PostgreSQL 16 | 5431 (host) |

## Como executar

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
    PASTO ||--o{ PIQUETE : possui
    PIQUETE ||--o{ ALOCADO : recebe
    ANIMAL ||--o{ ALOCADO : "é alocado em"

    USUARIO {
        usuarioid serial PK
        login varchar(50) UK
        senha varchar(100)
        removido boolean
    }

    PASTO {
        serial pastoid PK
        descricao varchar(100)
        areatotal numeric(10,2)
        removido boolean
    }

    PIQUETE {
        piqueteid serial PK
        descricao varchar(100)
        latitude numeric(10,7)
        longitude numeric(10,7)
        pastoidfk integer FK
        removido boolean
    }

    ANIMAL {
        animalid serial PK
        nome varchar(100)
        datanasc date
        removido boolean
    }

    ALOCADO {
        alocadoid serial PK
        animalidifk integer FK
        piqueteidfk integer FK
        datainicio date
        datafinal date
        removido boolean
    }
```

A tabela **ALOCADO** representa o relacionamento N:N entre animais e piquetes, registrando o período de permanência.


## Estrutura

```
backend/apps/<modulo>/controller + model   (pasto, piquete, animal, alocado, login)
frontend/apps/<modulo>/vw<Modulo>.js       (+ apps/shared: auth, api, crud, layout)
database/init.sql
```

## Contrato da API

Todas as rotas, exceto `POST /login`, exigem `Authorization: Bearer <jwt>` (401 se ausente/inválido). Datas em `YYYY-MM-DD`, campos numéricos como número JSON.

| Operação | Rota | Corpo | Resposta |
| --- | --- | --- | --- |
| Login | `POST /login` | `{login, senha}` | `{token, usuario}` |
| GetAllXXX | `GET /<tabela>` | — | lista (só `removido = false`) |
| GetXXXByID | `GET /<tabela>/<id>` | — | objeto ou 404 |
| InsertXXX | `POST /<tabela>` | campos da tabela | objeto criado (201) |
| UpdateXXX | `PUT /<tabela>/<id>` | campos da tabela | objeto atualizado |
| DeleteXXX | `DELETE /<tabela>/<id>` | — | `{mensagem}` (soft delete) |

Tabelas: `pasto`, `piquete`, `animal`, `alocado`. Erros devolvem `{erro: "texto"}`.

Campos (mesmos nomes do modelo relacional do trabalho):

- `pasto`: `pastoid`, `descricao`, `areatotal`
- `piquete`: `piqueteid`, `descricao`, `latitude`, `longitude`, `pastoidfk`
- `animal`: `animalid`, `nome`, `datanasc`
- `alocado`: `alocadoid`, `animalidifk`, `piqueteidfk`, `datainicio`, `datafinal` (opcional)

O back-end precisa liberar CORS para `http://localhost:3000`.
