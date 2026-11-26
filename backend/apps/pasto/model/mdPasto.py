from db import get_conexao


def listar():
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT pastoid, descricao, areatotal::float AS areatotal
        FROM pasto
        WHERE removido = FALSE
        ORDER BY pastoid
        """
    )
    dados = cur.fetchall()
    conn.close()
    return dados


def buscar(pastoid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT pastoid, descricao, areatotal::float AS areatotal
        FROM pasto
        WHERE pastoid = %s AND removido = FALSE
        """,
        (pastoid,),
    )
    pasto = cur.fetchone()
    conn.close()
    return pasto


def inserir(descricao, areatotal):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO pasto (descricao, areatotal)
        VALUES (%s, %s)
        RETURNING pastoid, descricao, areatotal::float AS areatotal
        """,
        (descricao, areatotal),
    )
    pasto = cur.fetchone()
    conn.commit()
    conn.close()
    return pasto


def atualizar(pastoid, descricao, areatotal):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE pasto
        SET descricao = %s, areatotal = %s
        WHERE pastoid = %s AND removido = FALSE
        RETURNING pastoid, descricao, areatotal::float AS areatotal
        """,
        (descricao, areatotal, pastoid),
    )
    pasto = cur.fetchone()
    conn.commit()
    conn.close()
    return pasto


def excluir(pastoid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE pasto SET removido = TRUE
        WHERE pastoid = %s AND removido = FALSE
        RETURNING pastoid
        """,
        (pastoid,),
    )
    apagado = cur.fetchone()
    conn.commit()
    conn.close()
    return apagado is not None