import os
import subprocess
import sys

def run_command(command, capture_output=True, shell=False):
    """Executes a command and optionally captures its output."""
    try:
        if capture_output:
            result = subprocess.run(command, shell=shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        else:
            subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def main():
    # Default destination for the qpull script is the current working directory
    destination = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    # Define project root directory as the current working directory
    project_root = os.getcwd()

    # Define paths
    venv_path = os.path.join(project_root, '.venv')
    requirements_path = os.path.join(project_root, 'requirements.txt')
    wrapper_path = os.path.join(destination, 'qpull')

    # Check if qpull already exists at the destination
    if os.path.isfile(wrapper_path):
        print(f"Updating existing qpull script at {wrapper_path}")
    else:
        print(f"Creating new qpull script at {wrapper_path}")

    # Create or update the qpull script
    with open(wrapper_path, 'w') as wrapper_file:
        wrapper_file.write(f"""#!/usr/bin/env python3
import os
import subprocess
import sys

def run_script():
    subprocess.run([r"{os.path.join(venv_path, 'bin' if os.name != 'nt' else 'Scripts', 'python')}", r"{os.path.join(project_root, 'qpull.py')}"] + sys.argv[1:])

if __name__ == '__main__':
    run_script()
""")

    # Set execute permissions for qpull (Unix-based systems)
    if os.name != 'nt':
        os.chmod(wrapper_path, 0o755)

    # Create the virtual environment if it doesn't exist
    if not os.path.isdir(venv_path):
        print("Creating virtual environment...")
        run_command(['python', '-m', 'venv', venv_path], shell=False)

    # Install requirements
    if os.path.isfile(requirements_path):
        print("Installing dependencies from requirements.txt...")
        python_executable = os.path.join(venv_path, 'bin' if os.name != 'nt' else 'Scripts', 'python')
        requirements_command = [python_executable, '-m', 'pip', 'install', '-r', requirements_path]

        # Run the command without capturing output for real-time display
        run_command(requirements_command, capture_output=False, shell=False)
    else:
        print("requirements.txt not found, skipping dependency installation.")

    print("Setup completed. The qpull script is located at", wrapper_path)

if __name__ == "__main__":
    main()
