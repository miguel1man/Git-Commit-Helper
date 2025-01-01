import datetime
import os
import subprocess
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

    # Mostrar último commit
    print("\nÚltimo commit:")
    last_commit = run_git_command(["git", "log", "-1", "--pretty=format:%h - %s"])
    if last_commit:
        print("-" * 40)  # Línea separadora para mejor legibilidad

    # Ejecutar git status
    print("\nEjecutando git status:")
    status_output = run_git_command(["git", "status"])

    # Obtener la fecha actual
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Preparar el mensaje de commit
    commit_message = f"backup {current_date}"

    # Preguntar si desea continuar después de ver el status
    choice = (
        input(f"\n¿Desea crear un commit '{commit_message}'? ([Y]/n): ").lower().strip()
    )
    if choice == "n":
        print("Operación cancelada.")
        return

    while True:

        # Si el usuario solo presiona Enter, asignar 'y' como valor por defecto
        if choice == "":
            choice = "y"

        if choice not in ["y", "n"]:
            print("Opción no válida. Por favor, selecciona 'y', 'n'")
            continue

        if choice == "y":
            # Ejecutar git commit
            run_git_command(["git", "add", "."])
            run_git_command(["git", "commit", "-m", commit_message])

            # Ejecutar git push
            run_git_command(["git", "push"])
            print("Commit y push completados con éxito.")
            break


if __name__ == "__main__":
    user_input = input(
        f"Ingresa la ruta del proyecto (presiona Enter para usar la ruta por defecto '{DEFAULT_PROJECT_PATH}'): "
    )
    project_path = user_input.strip() if user_input.strip() else DEFAULT_PROJECT_PATH
    git_backup(project_path)
