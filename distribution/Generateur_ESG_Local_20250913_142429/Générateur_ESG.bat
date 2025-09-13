@echo off
setlocal enabledelayedexpansion

:: Configuration de l'apparence
title Générateur ESG - Streamlit
color 0A

echo.
echo =====================================
echo    GÉNÉRATEUR ESG - STREAMLIT
echo =====================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH
    echo.
    echo 📥 Veuillez installer Python depuis https://python.org
    echo ⚠️  IMPORTANT: Cochez "Add to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

:: Afficher la version de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% détecté

:: Aller dans le répertoire du script
cd /d "%~dp0"
echo 📁 Dossier: %CD%

echo.
echo 🚀 Lancement de l'application...
echo.

:: Lancer le script Python
python launch_app.py

:: Si le script Python échoue, essayer le mode de compatibilité
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Mode de compatibilité activé...
    echo.
    
    :: Installation des dépendances
    echo 📦 Installation des dépendances...
    python -m pip install streamlit openpyxl xlwings pandas --quiet
    
    :: Lancement direct de Streamlit
    echo 🚀 Lancement direct de Streamlit...
    python -m streamlit run app.py --server.port=8501 --browser.gatherUsageStats=false
)

pause