from getpass import getpass

from app.services.usuario_service import (
    cambiar_estado_usuario,
    crear_usuario,
    listar_usuarios,
)


def crear():
    username = input("Usuario: ").strip()

    if not username:
        print("El usuario no puede estar vacío.")
        return

    password = getpass("Contraseña: ")

    if not password:
        print("La contraseña no puede estar vacía.")
        return

    confirmacion = getpass("Repite la contraseña: ")

    if password != confirmacion:
        print("Las contraseñas no coinciden.")
        return

    usuario = crear_usuario(
        username=username,
        password=password,
    )

    if usuario is None:
        print(f"El usuario '{username}' ya existe.")
        return

    print(f"Usuario '{username}' creado correctamente.")


def activar_desactivar():
    usuarios = listar_usuarios()

    if not usuarios:
        print("No hay usuarios registrados.")
        return

    print()
    print("Usuarios")
    print("--------")

    for usuario in usuarios:
        estado = "ACTIVO" if usuario["activo"] else "INACTIVO"

        print(
            f'{usuario["id"]}. '
            f'{usuario["username"]} '
            f'[{estado}]'
        )

    print()

    valor = input(
        "ID del usuario a activar/desactivar: "
    ).strip()

    if not valor.isdigit():
        print("Debes ingresar un ID válido.")
        return

    usuario_id = int(valor)

    nuevo_estado = cambiar_estado_usuario(usuario_id)

    if nuevo_estado is None:
        print("Usuario no encontrado.")
        return

    estado = "activado" if nuevo_estado else "desactivado"

    print(f"Usuario {estado} correctamente.")


def main():
    while True:
        print()
        print("Administración de usuarios")
        print("--------------------------")
        print("1. Crear usuario")
        print("2. Activar/desactivar usuario")
        print("3. Salir")
        print()

        opcion = input("Opción: ").strip()

        if opcion == "1":
            crear()

        elif opcion == "2":
            activar_desactivar()

        elif opcion == "3":
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()