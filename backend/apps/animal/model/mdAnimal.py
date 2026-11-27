from db import get_conexao


def listar():
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT animalid, nome, datanasc::text AS datanasc
        FROM animal
        WHERE removido = FALSE
        ORDER BY animalid
        """
    )
    dados = cur.fetchall()
    conn.close()
    return dados


def buscar(animalid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT animalid, nome, datanasc::text AS datanasc
        FROM animal
        WHERE animalid = %s AND removido = FALSE
        """,
        (animalid,),
    )
    animal = cur.fetchone()
    conn.close()
    return animal


def inserir(nome, datanasc):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO animal (nome, datanasc)
        VALUES (%s, %s)
        RETURNING animalid, nome, datanasc::text AS datanasc
        """,
        (nome, datanasc),
    )
    animal = cur.fetchone()
    conn.commit()
    conn.close()
    return animal


def atualizar(animalid, nome, datanasc):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE animal
        SET nome = %s, datanasc = %s
        WHERE animalid = %s AND removido = FALSE
        RETURNING animalid, nome, datanasc::text AS datanasc
        """,
        (nome, datanasc, animalid),
    )
    animal = cur.fetchone()
    conn.commit()
    conn.close()
    return animal


def excluir(animalid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE animal SET removido = TRUE
        WHERE animalid = %s AND removido = FALSE
        RETURNING animalid
        """,
        (animalid,),
    )
    apagado = cur.fetchone()
    conn.commit()
    conn.close()
    return apagado is not None