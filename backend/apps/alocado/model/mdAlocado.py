from db import get_conexao


def listar():
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT alocadoid, animalidifk, piqueteidfk,
               datainicio::text AS datainicio, datafinal::text AS datafinal
        FROM alocado
        WHERE removido = FALSE
        ORDER BY alocadoid
        """
    )
    dados = cur.fetchall()
    conn.close()
    return dados


def buscar(alocadoid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT alocadoid, animalidifk, piqueteidfk,
               datainicio::text AS datainicio, datafinal::text AS datafinal
        FROM alocado
        WHERE alocadoid = %s AND removido = FALSE
        """,
        (alocadoid,),
    )
    alocado = cur.fetchone()
    conn.close()
    return alocado


def inserir(animalidifk, piqueteidfk, datainicio, datafinal):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO alocado (animalidifk, piqueteidfk, datainicio, datafinal)
        VALUES (%s, %s, %s, %s)
        RETURNING alocadoid, animalidifk, piqueteidfk,
                  datainicio::text AS datainicio, datafinal::text AS datafinal
        """,
        (animalidifk, piqueteidfk, datainicio, datafinal),
    )
    alocado = cur.fetchone()
    conn.commit()
    conn.close()
    return alocado


def atualizar(alocadoid, animalidifk, piqueteidfk, datainicio, datafinal):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE alocado
        SET animalidifk = %s, piqueteidfk = %s, datainicio = %s, datafinal = %s
        WHERE alocadoid = %s AND removido = FALSE
        RETURNING alocadoid, animalidifk, piqueteidfk,
                  datainicio::text AS datainicio, datafinal::text AS datafinal
        """,
        (animalidifk, piqueteidfk, datainicio, datafinal, alocadoid),
    )
    alocado = cur.fetchone()
    conn.commit()
    conn.close()
    return alocado


def excluir(alocadoid):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE alocado SET removido = TRUE
        WHERE alocadoid = %s AND removido = FALSE
        RETURNING alocadoid
        """,
        (alocadoid,),
    )
    apagado = cur.fetchone()
    conn.commit()
    conn.close()
    return apagado is not None