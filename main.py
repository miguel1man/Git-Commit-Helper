import subprocess
import datetime
import os
from dotenv import load_dotenv


load_dotenv()


DEFAULT_PROJECT_PATH = os.getenv("DEFAULT_PROJECT_PATH")


def run_git_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Comando ejecutado con éxito: {' '.join(command)}")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return None


def get_user_choice(prompt, options):
    while True:
        choice = input(prompt).lower()
        if choice in options:
            return choice
        print(
            f"Por favor, ingresa una de las siguientes opciones: {', '.join(options)}"
        )


def git_backup(project_path):
    # Cambiar al directorio del proyecto
    try:
        os.chdir(project_path)
        print(f"Cambiado al directorio: {project_path}")
    except FileNotFoundError:
        print(f"Error: El directorio {project_path} no existe.")
        return
    except PermissionError:
        print(f"Error: No tienes permisos para acceder al directorio {project_path}.")
        return

    # Obtener la fecha actual
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Ejecutar git status
    print("Ejecutando git status:")
    run_git_command(["git", "status"])

    # Ejecutar git add .
    run_git_command(["git", "add", "."])

    # Preparar el mensaje de commit
    commit_message = f"backup {current_date}"

    while True:
        # Mostrar el mensaje de commit actual y pedir confirmación
        print(f"\nMensaje de commit actual: {commit_message}")
        choice = get_user_choice(
            "¿Deseas continuar con este mensaje? (y: aceptar, n: cancelar, e: editar): ",
            ["y", "n", "e"],
        )

        if choice == "y":
            # Ejecutar git commit
            run_git_command(["git", "commit", "-m", commit_message])

            # Ejecutar git push
            run_git_command(["git", "push"])
            print("Commit y push completados con éxito.")
            break

        elif choice == "n":
            # Cancelar la operación
            print("Operación cancelada.")
            return

        elif choice == "e":
            # Editar el mensaje de commit
            new_message = input("Ingresa el nuevo mensaje de commit: ")
            if new_message.strip():  # Asegurarse de que el nuevo mensaje no esté vacío
                commit_message = new_message
            else:
                print(
                    "El mensaje de commit no puede estar vacío. Se mantendrá el mensaje anterior."
                )


if __name__ == "__main__":
    user_input = input(
        f"Ingresa la ruta del proyecto (presiona Enter para usar la ruta por defecto '{DEFAULT_PROJECT_PATH}'): "
    )
    project_path = user_input.strip() if user_input.strip() else DEFAULT_PROJECT_PATH
    git_backup(project_path)
