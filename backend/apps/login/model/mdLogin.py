from db import get_conexao

def buscar_usuario(login, senha):
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT usuarioid, login
        FROM usuario
        WHERE login = %s AND senha = %s AND removido = FALSE
        """,
        (login, senha),
    )
    usuario = cur.fetchone()
    conn.close()
    return usuario