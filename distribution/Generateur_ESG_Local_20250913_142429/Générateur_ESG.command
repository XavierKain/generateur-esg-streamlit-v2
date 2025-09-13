#!/bin/bash

# Configuration
clear
echo "====================================="
echo "   GÉNÉRATEUR ESG - STREAMLIT"
echo "====================================="
echo

# Couleurs pour le terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Aller dans le répertoire du script
cd "$(dirname "$0")"
echo "📁 Dossier: $(pwd)"
echo

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Vérifier Python
if command_exists python3; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python $PYTHON_VERSION détecté${NC}"
elif command_exists python; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python $PYTHON_VERSION détecté${NC}"
else
    echo -e "${RED}❌ Python n'est pas installé${NC}"
    echo "📥 Veuillez installer Python depuis https://python.org"
    echo
    read -p "Appuyez sur Entrée pour fermer..."
    exit 1
fi

echo
echo "🚀 Lancement de l'application..."
echo

# Lancer le script Python
$PYTHON_CMD launch_app.py

# Si le script Python échoue, essayer le mode de compatibilité
if [ $? -ne 0 ]; then
    echo
    echo -e "${YELLOW}⚠️  Mode de compatibilité activé...${NC}"
    echo
    
    # Installation des dépendances
    echo "📦 Installation des dépendances..."
    $PYTHON_CMD -m pip install streamlit openpyxl xlwings pandas --quiet
    
    # Lancement direct de Streamlit
    echo "🚀 Lancement direct de Streamlit..."
    $PYTHON_CMD -m streamlit run app.py --server.port=8501 --browser.gatherUsageStats=false
fi

echo
read -p "Appuyez sur Entrée pour fermer..."