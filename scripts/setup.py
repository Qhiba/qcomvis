import os
import sys
import subprocess

def install_req():
    project_root = os.path.abspath(os.getcwd())
    venv_path = os.path.join(project_root, '.env')

    if not os.path.exists(venv_path):
        print("WARNING: Virtual Environment not found. Creating one...\n")
        subprocess.check_call([sys.executable, '-m', 'venv', '.env'])
        print(f"\nINFO: Virtual environment created at {venv_path}\n")

    req_path = os.path.join(project_root, 'requirements.txt')
    if os.path.exists(req_path):
        print("INFO: Installing dependencies in the virtual environment...\n")
        pip_path = os.path.join(venv_path, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(venv_path, 'bin', pip)
        subprocess.check_call([pip_path, 'install', '-r', req_path])
        print("\nINFO: Dependencies installed.\n")
    else:
        print("\nERROR: requirements.txt not found in the project root. Skipping dependency installation. Run 'git pull origin master' to pull requirements.txt.\n")
    

if __name__ == "__main__":
    try:
        install_req()
    except Exception as e:
        print(f"ERROR: {e}")
