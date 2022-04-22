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
# Seulement s'il n'est pas déjà présent, car parfois on peut être amené à
# réinstaller le venv et donc réexecuter le script
first_line=$(head -1 main.py)
she_bang="#! $VENV_NAME/bin/python"

if [[ $first_line != $she_bang ]]; then
    sed -i "1i$she_bang\n" main.py
fi

# On le rend exécutable
chmod +x main.py

echo "Vous pouvez entrer './main.py' pour démarrer Wirefish :)"
