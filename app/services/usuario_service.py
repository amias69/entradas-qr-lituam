import sqlite3

from app.db.database import get_connection
from app.services.auth_service import (
    generar_password_hash,
    verificar_password,
)


def crear_usuario(username, password):
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO usuarios (
                    username,
                    password_hash
                )
                VALUES (?, ?)
                """,
                (
                    username,
                    generar_password_hash(password),
                ),
            )

            usuario_id = cursor.lastrowid

            return connection.execute(
                """
                SELECT *
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            ).fetchone()

    except sqlite3.IntegrityError as error:
        if "usuarios.username" in str(error):
            return None

        raise


def buscar_usuario(username):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM usuarios
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

def autenticar_usuario(username, password):
    usuario = buscar_usuario(username)

    if usuario is None:
        return None

    if not usuario["activo"]:
        return None

    if not verificar_password(
        password,
        usuario["password_hash"],
    ):
        return None

    return usuario


def desactivar_usuario(username):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE usuarios
            SET activo = 0
            WHERE username = ?
              AND activo = 1
            """,
            (username,),
        )

        return cursor.rowcount == 1

def listar_usuarios():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                id,
                username,
                activo,
                creado_en
            FROM usuarios
            ORDER BY username COLLATE NOCASE
            """
        ).fetchall()


def cambiar_estado_usuario(usuario_id):
    with get_connection() as connection:
        usuario = connection.execute(
            """
            SELECT activo
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()

        if usuario is None:
            return None

        nuevo_estado = 0 if usuario["activo"] else 1

        connection.execute(
            """
            UPDATE usuarios
            SET activo = ?
            WHERE id = ?
            """,
            (
                nuevo_estado,
                usuario_id,
            ),
        )

        return nuevo_estado

def buscar_usuario_por_id(usuario_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM usuarios
            WHERE id = ?
            """,
            (usuario_id,),
        ).fetchone()