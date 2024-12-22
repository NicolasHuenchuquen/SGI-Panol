import subprocess
import webbrowser
import os

def install_requirements():
    """Instala las dependencias del archivo requirements.txt."""
    print("Instalando dependencias...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

def apply_migrations():
    """Ejecuta las migraciones de la base de datos."""
    print("Aplicando migraciones...")
    subprocess.run(["python", "manage.py", "migrate"], check=True)

def run_server():
    """Ejecuta el servidor de desarrollo de Django."""
    print("Iniciando el servidor de Django...")
    server_process = subprocess.Popen(["python", "manage.py", "runserver"])
    return server_process

def open_browser():
    """Abre el navegador en la dirección predeterminada del servidor."""
    print("Abriendo navegador...")
    url = "http://127.0.0.1:8000"
    webbrowser.open(url)

if __name__ == "__main__":
    try:
        install_requirements()
        apply_migrations()
        server_process = run_server()
        open_browser()
        
        print("Presiona Ctrl+C para detener el servidor.")
        server_process.wait()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        server_process.terminate()
    except Exception as e:
        print(f"Error: {e}")
