import sqlite3

from app.db.database import get_connection
from app.services.token_service import generar_token


def crear_entrada(nombre, telefono, forma_pago, generado_por):
    while True:
        token = generar_token()

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO entradas (
                        token,
                        nombre,
                        telefono,
                        forma_pago,
                        generado_por
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        token,
                        nombre,
                        telefono,
                        forma_pago,
                        generado_por,
                    ),
                )

                entrada_id = cursor.lastrowid

                connection.execute(
                    """
                    INSERT INTO historial_entradas (
                        entrada_id,
                        usuario_id,
                        accion
                    )
                    VALUES (?, ?, 'CREADA')
                    """,
                    (
                        entrada_id,
                        generado_por,
                    ),
                )

                return connection.execute(
                    """
                    SELECT *
                    FROM entradas
                    WHERE id = ?
                    """,
                    (entrada_id,),
                ).fetchone()

        except sqlite3.IntegrityError as error:
            if "entradas.token" in str(error):
                continue

            raise


def buscar_por_token(token):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM entradas
            WHERE token = ?
            """,
            (token,),
        ).fetchone()


def buscar_entradas(consulta):
    consulta = consulta.strip()

    if not consulta:
        return []

    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM entradas
            WHERE estado != 'ANULADA'
              AND (
                    token = ?
                 OR telefono = ?
                 OR nombre LIKE ?
              )
            ORDER BY creada_en DESC
            """,
            (
                consulta,
                consulta,
                f"%{consulta}%",
            ),
        ).fetchall()


def editar_entrada(
    entrada_id,
    nombre,
    telefono,
    forma_pago,
    usuario_id,
):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE entradas
            SET nombre = ?,
                telefono = ?,
                forma_pago = ?
            WHERE id = ?
            """,
            (
                nombre,
                telefono,
                forma_pago,
                entrada_id,
            ),
        )

        if cursor.rowcount == 0:
            return None

        connection.execute(
            """
            INSERT INTO historial_entradas (
                entrada_id,
                usuario_id,
                accion
            )
            VALUES (?, ?, 'EDITADA')
            """,
            (
                entrada_id,
                usuario_id,
            ),
        )

        return connection.execute(
            """
            SELECT *
            FROM entradas
            WHERE id = ?
            """,
            (entrada_id,),
        ).fetchone()

def anular_entrada(entrada_id, usuario_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE entradas
            SET estado = 'ANULADA'
            WHERE id = ?
              AND estado = 'ACTIVA'
            """,
            (entrada_id,),
        )

        if cursor.rowcount == 0:
            return None

        connection.execute(
            """
            INSERT INTO historial_entradas (
                entrada_id,
                usuario_id,
                accion
            )
            VALUES (?, ?, 'ANULADA')
            """,
            (
                entrada_id,
                usuario_id,
            ),
        )

        return connection.execute(
            """
            SELECT *
            FROM entradas
            WHERE id = ?
            """,
            (entrada_id,),
        ).fetchone()

def validar_entrada(token, usuario_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE entradas
            SET estado = 'USADA',
                usada_en = CURRENT_TIMESTAMP
            WHERE token = ?
              AND estado = 'ACTIVA'
            """,
            (token,),
        )

        if cursor.rowcount == 0:
            return None

        entrada = connection.execute(
            """
            SELECT *
            FROM entradas
            WHERE token = ?
            """,
            (token,),
        ).fetchone()

        connection.execute(
            """
            INSERT INTO historial_entradas (
                entrada_id,
                usuario_id,
                accion
            )
            VALUES (?, ?, 'VALIDADA')
            """,
            (
                entrada["id"],
                usuario_id,
            ),
        )

        return entrada

def listar_asistentes():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                nombre,
                telefono,
                forma_pago,
                token,
                estado
            FROM entradas
            WHERE estado != 'ANULADA'
            ORDER BY nombre COLLATE NOCASE
            """
        ).fetchall()

def obtener_historial(entrada_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                historial_entradas.accion,
                historial_entradas.fecha,
                usuarios.username
            FROM historial_entradas
            JOIN usuarios
                ON usuarios.id = historial_entradas.usuario_id
            WHERE historial_entradas.entrada_id = ?
            ORDER BY historial_entradas.fecha ASC
            """,
            (entrada_id,),
        ).fetchall()