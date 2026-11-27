from db import get_conexao


def buscar_usuario(login):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT usuarioid, login, senha
        FROM usuario
        WHERE login = %s AND removido = FALSE
        """,
        (login,),
    )
    usuario = cur.fetchone()
    conn.close()
    return usuario