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
where python >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>&1
    if %errorlevel% == 0 (
        set PYTHON_CMD=python3
    ) else (
        echo ❌ ERREUR: Python n'est pas installé ou pas dans le PATH
        echo.
        echo 📥 Veuillez installer Python depuis https://python.org
        echo ⚠️  IMPORTANT: Cochez "Add to PATH" lors de l'installation
        echo.
        pause
        exit /b 1
    )
)

:: Vérifier s'il y a un environnement virtuel
set VENV_PYTHON=
if exist "..\\.venv\\Scripts\\python.exe" (
    set VENV_PYTHON=..\.venv\Scripts\python.exe
    echo ✅ Environnement virtuel détecté
) else if exist ".venv\\Scripts\\python.exe" (
    set VENV_PYTHON=.venv\Scripts\python.exe
    echo ✅ Environnement virtuel détecté
) else if exist "venv\\Scripts\\python.exe" (
    set VENV_PYTHON=venv\Scripts\python.exe
    echo ✅ Environnement virtuel détecté
)

:: Utiliser l'environnement virtuel si disponible
if defined VENV_PYTHON (
    set PYTHON_CMD=%VENV_PYTHON%
    for /f "tokens=2" %%v in ('"%PYTHON_CMD%" --version 2^>^&1') do set PYTHON_VERSION=%%v
    echo ✅ Python %PYTHON_VERSION% ^(venv^)
) else (
    for /f "tokens=2" %%v in ('"%PYTHON_CMD%" --version 2^>^&1') do set PYTHON_VERSION=%%v
    echo ✅ Python %PYTHON_VERSION% ^(système^)
)

:: Aller dans le répertoire du script
cd /d "%~dp0"
echo 📁 Dossier: %CD%

echo.
echo 🚀 Lancement de l'application...
echo.

:: Lancer le script Python
"%PYTHON_CMD%" launch_app.py

:: Si le script Python échoue, essayer le mode de compatibilité
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Mode de compatibilité activé...
    echo.
    
    :: Installation des dépendances
    echo 📦 Installation des dépendances...
    "%PYTHON_CMD%" -m pip install streamlit openpyxl xlwings pandas --quiet
    
    :: Lancement direct de Streamlit
    echo 🚀 Lancement direct de Streamlit...
    "%PYTHON_CMD%" -m streamlit run app.py --server.port=8501 --browser.gatherUsageStats=false
)

pause