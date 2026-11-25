CREATE TABLE usuario (
    usuarioid SERIAL PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    removido BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE pasto (
    pastoid SERIAL PRIMARY KEY,
    descricao VARCHAR(100)  NOT NULL,
    areatotal NUMERIC(10,2) NOT NULL,
    removido  BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE piquete (
    piqueteid SERIAL PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    latitude NUMERIC(10,7) NOT NULL,
    longitude NUMERIC(10,7) NOT NULL,
    pastoidfk INTEGER NOT NULL REFERENCES pasto(pastoid),
    removido BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE animal (
    animalid SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    datanasc DATE NOT NULL,
    removido BOOLEAN NOT NULL DEFAULT FALSE
);

-- tabela resultante do relacionamento N:N entre animal e piquete
CREATE TABLE alocado (
    alocadoid SERIAL PRIMARY KEY,
    animalidifk INTEGER NOT NULL REFERENCES animal(animalid),
    piqueteidfk INTEGER NOT NULL REFERENCES piquete(piqueteid),
    datainicio DATE NOT NULL,
    datafinal DATE,
    removido BOOLEAN NOT NULL DEFAULT FALSE,
    CHECK (datafinal IS NULL OR datafinal >= datainicio)
);

-- usuário inicial: login dw3 / senha dw3
INSERT INTO usuario (login, senha) VALUES ('dw3', 'dw3');