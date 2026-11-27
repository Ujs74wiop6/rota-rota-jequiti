from db import get_conexao


def listar():
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT piqueteid, descricao, latitude::float AS latitude,
               longitude::float AS longitude, pastoidfk
        FROM piquete
        WHERE removido = FALSE
        ORDER BY piqueteid
        """
    )
    dados = cur.fetchall()
    conn.close()
    return dados


def buscar(piqueteid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT piqueteid, descricao, latitude::float AS latitude,
               longitude::float AS longitude, pastoidfk
        FROM piquete
        WHERE piqueteid = %s AND removido = FALSE
        """,
        (piqueteid,),
    )
    piquete = cur.fetchone()
    conn.close()
    return piquete


def inserir(descricao, latitude, longitude, pastoidfk):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO piquete (descricao, latitude, longitude, pastoidfk)
        VALUES (%s, %s, %s, %s)
        RETURNING piqueteid, descricao, latitude::float AS latitude,
                  longitude::float AS longitude, pastoidfk
        """,
        (descricao, latitude, longitude, pastoidfk),
    )
    piquete = cur.fetchone()
    conn.commit()
    conn.close()
    return piquete


def atualizar(piqueteid, descricao, latitude, longitude, pastoidfk):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE piquete
        SET descricao = %s, latitude = %s, longitude = %s, pastoidfk = %s
        WHERE piqueteid = %s AND removido = FALSE
        RETURNING piqueteid, descricao, latitude::float AS latitude,
                  longitude::float AS longitude, pastoidfk
        """,
        (descricao, latitude, longitude, pastoidfk, piqueteid),
    )
    piquete = cur.fetchone()
    conn.commit()
    conn.close()
    return piquete


def excluir(piqueteid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE piquete SET removido = TRUE
        WHERE piqueteid = %s AND removido = FALSE
        RETURNING piqueteid
        """,
        (piqueteid,),
    )
    apagado = cur.fetchone()
    conn.commit()
    conn.close()
    return apagado is not None