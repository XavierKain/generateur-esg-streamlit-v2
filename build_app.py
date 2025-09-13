#!/usr/bin/env python3
"""
Script pour créer une application .app sur macOS
"""

import os
import sys
import shutil
from pathlib import Path

def create_macos_app():
    """Créer une application .app pour macOS"""
    
    app_name = "Générateur ESG"
    app_dir = Path(f"{app_name}.app")
    
    # Créer la structure .app
    contents_dir = app_dir / "Contents"
    macos_dir = contents_dir / "MacOS"
    resources_dir = contents_dir / "Resources"
    
    # Créer les dossiers
    macos_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.esg.generator</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>"""
    
    with open(contents_dir / "Info.plist", "w") as f:
        f.write(info_plist)
    
    # Créer le script exécutable
    executable_script = f"""#!/bin/bash
cd "$(dirname "$0")/../../../"
python3 launch_app.py
"""
    
    executable_path = macos_dir / app_name
    with open(executable_path, "w") as f:
        f.write(executable_script)
    
    # Rendre le script exécutable
    os.chmod(executable_path, 0o755)
    
    print(f"✅ Application {app_name}.app créée avec succès !")
    print(f"📁 Emplacement: {app_dir.absolute()}")
    print("🚀 Double-cliquez sur l'application pour la lancer")

if __name__ == "__main__":
    if sys.platform == "darwin":
        create_macos_app()
    else:
        print("❌ Ce script est destiné à macOS uniquement")