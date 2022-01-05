VENV_NAME="scapy-venv"
MAIN_FILE="main.py"

python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate
pip install -r requirements.txt
sed -i "1i#! $VENV_NAME/bin/python\n" main.py
chmod +x main.py

echo "You can use './main.py' to start the script"
