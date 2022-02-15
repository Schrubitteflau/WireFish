VENV_NAME="wirefish-venv"

if [ -d "$VENV_NAME" ]; then
    echo "venv '$VENV_NAME' déjà installé dans le dossier courant"
    exit
fi

python3 -m venv $VENV_NAME
# Activation du venv (met à jour et ajoute des variables d'environnement)
source $VENV_NAME/bin/activate
# Installation des dépendances
pip install wheel
pip install -r requirements.txt
# Ajout du she-bang pointant vers le binaire du venv au début de main.py
sed -i "1i#! $VENV_NAME/bin/python\n" main.py
# On le rend exécutable
chmod +x main.py

echo "Vous pouvez entrer './main.py' pour démarrer Wirefish :)"
