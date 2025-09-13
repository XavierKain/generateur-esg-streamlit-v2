#!/usr/bin/env python3
"""
Test launcher sans threading - Diagnostic
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
from pathlib import Path

class SimpleTestLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test Launcher Sans Threading")
        self.root.geometry("400x300")
        
        # Trouver le bon Python
        venv_paths = [
            "../.venv/bin/python",
            ".venv/bin/python", 
            "venv/bin/python"
        ]
        
        self.python_executable = sys.executable  # fallback
        
        for venv_path in venv_paths:
            full_path = Path(venv_path)
            print(f"Test du chemin: {full_path} (existe: {full_path.exists()})")
            if full_path.exists():
                self.python_executable = str(full_path.absolute())
                print(f"✅ Venv trouvé: {self.python_executable}")
                break
        else:
            print(f"⚠️ Pas de venv trouvé, utilisation du système: {self.python_executable}")
            
        self.setup_ui()
        
    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Test SANS Threading").grid(row=0, column=0, pady=10)
        
        ttk.Label(frame, text=f"Python: {self.python_executable}", wraplength=350).grid(row=1, column=0, pady=5)
        
        self.status_label = ttk.Label(frame, text="Prêt")
        self.status_label.grid(row=2, column=0, pady=10)
        
        self.result_text = tk.Text(frame, height=8, width=50)
        self.result_text.grid(row=3, column=0, pady=10)
        
        ttk.Button(frame, text="Test Python Version", command=self.test_python).grid(row=4, column=0, pady=5)
        ttk.Button(frame, text="Test Streamlit", command=self.test_streamlit).grid(row=5, column=0, pady=5)
        
    def log_result(self, message):
        self.result_text.insert(tk.END, message + "\\n")
        self.result_text.see(tk.END)
        self.root.update()
        
    def test_python(self):
        print("TEST: test_python appelée")
        self.status_label.config(text="Test Python en cours...")
        self.log_result("=== Test Python Version ===")
        
        try:
            result = subprocess.run([self.python_executable, "--version"], 
                                  capture_output=True, text=True, timeout=10)
            self.log_result(f"Sortie: {result.stdout.strip()}")
            if result.stderr:
                self.log_result(f"Erreurs: {result.stderr.strip()}")
            self.status_label.config(text="✅ Test Python OK")
            
        except Exception as e:
            self.log_result(f"ERREUR: {e}")
            self.status_label.config(text=f"❌ Erreur: {e}")
        
        print("FIN: test_python")
        
    def test_streamlit(self):
        print("TEST: test_streamlit appelée")
        self.status_label.config(text="Test Streamlit en cours...")
        self.log_result("=== Test Streamlit ===")
        
        try:
            result = subprocess.run([self.python_executable, "-c", "import streamlit; print(f'Streamlit {streamlit.__version__} OK')"], 
                                  capture_output=True, text=True, timeout=10)
            self.log_result(f"Sortie: {result.stdout.strip()}")
            if result.stderr:
                self.log_result(f"Erreurs: {result.stderr.strip()}")
            self.status_label.config(text="✅ Test Streamlit OK")
            
        except Exception as e:
            self.log_result(f"ERREUR: {e}")
            self.status_label.config(text=f"❌ Erreur: {e}")
        
        print("FIN: test_streamlit")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Démarrage du test launcher SANS threading...")
    launcher = SimpleTestLauncher()
    launcher.run()