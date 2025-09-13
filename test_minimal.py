#!/usr/bin/env python3
"""
Diagnostic très simple - étape par étape
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
from pathlib import Path

class MinimalTest:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test Minimal")
        self.root.geometry("300x200")
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Test Minimal").pack(pady=10)
        
        self.status = ttk.Label(frame, text="Prêt")
        self.status.pack(pady=10)
        
        ttk.Button(frame, text="Test 1: Message simple", command=self.test1).pack(pady=5)
        ttk.Button(frame, text="Test 2: Python version", command=self.test2).pack(pady=5)
        
    def test1(self):
        print("DEBUT test1")
        self.status.config(text="Test 1 exécuté !")
        print("FIN test1")
        
    def test2(self):
        print("DEBUT test2")
        self.status.config(text="Test 2 en cours...")
        
        try:
            # Test très simple
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            print(f"Résultat: {result.stdout.strip()}")
            self.status.config(text=f"Version: {result.stdout.strip()}")
        except Exception as e:
            print(f"ERREUR: {e}")
            self.status.config(text=f"Erreur: {e}")
        
        print("FIN test2")
        
    def run(self):
        print("Démarrage interface...")
        self.root.mainloop()

if __name__ == "__main__":
    test = MinimalTest()
    test.run()