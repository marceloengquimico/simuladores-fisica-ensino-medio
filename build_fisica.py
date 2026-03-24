#!/usr/bin/env python3
"""
build.py — Compila fisica_simulador.py em executável

USO:
    1. pip install -r requirements.txt
    2. python build.py

Saída:
    dist/FisicaSimulador.exe   (Windows)
    dist/FisicaSimulador       (Linux/macOS)
"""

import subprocess, sys, os

def build():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "FisicaSimulador",
        "--clean",
        "fisica_simulador.py"
    ]
    print("=" * 50)
    print("  Build: Simulador de Física")
    print("=" * 50)
    result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        exe = "dist/FisicaSimulador.exe" if sys.platform=="win32" else "dist/FisicaSimulador"
        print(f"\n  ✓  Executável gerado: {exe}")
    else:
        print("\n  ✗  Falhou. Rode:  pip install pyinstaller")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
