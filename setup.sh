#!/bin/bash

# Default destination for the qpull script is the current working directory
DESTINATION=${1:-$(pwd)}

# Define project root directory as the current working directory
PROJECT_ROOT=$(pwd)

# Define paths
VENV_PATH="$PROJECT_ROOT/.venv"
REQUIREMENTS_PATH="$PROJECT_ROOT/requirements.txt"
WRAPPER_PATH="$DESTINATION/qpull"

# Check if qpull already exists at the destination
if [ -f "$WRAPPER_PATH" ]; then
    echo "Updating existing qpull script at $WRAPPER_PATH"
else
    echo "Creating new qpull script at $WRAPPER_PATH"
fi

# Create or update the qpull script
cat << EOF > "$WRAPPER_PATH"
#!/bin/bash
# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python script
"$PROJECT_ROOT/qpull.py" "\$@"

# Deactivate the virtual environment
deactivate
EOF

# Set execute permissions for qpull
chmod u+x "$WRAPPER_PATH"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install requirements
if [ -f "$REQUIREMENTS_PATH" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -q -r "$REQUIREMENTS_PATH"
else
    echo "requirements.txt not found, skipping dependency installation."
fi

# Deactivate the virtual environment
deactivate

# Output warnings
echo "WARNING: If you move the location of the project directory, you will need to run this setup script again."

echo "Setup completed. The qpull script is located at $WRAPPER_PATH"
