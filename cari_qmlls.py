import os
import sys
from pathlib import Path

# Biasanya ada di dalam folder Scripts (Windows) atau bin (Linux/Mac) di dalam venv
venv_path = Path(sys.prefix)
if os.name == 'nt': # Windows
    potential_path = venv_path / "Lib" / "site-packages" / "PySide6" / "qmlls.exe"
    # Cek juga di folder Scripts jika tidak ada di site-packages
    if not potential_path.exists():
        potential_path = venv_path / "Scripts" / "qmlls.exe"
else: # Mac/Linux
    potential_path = venv_path / "bin" / "qmlls"

print("-" * 30)
if potential_path.exists():
    print("PATH DITEMUKAN (Copy ini ke settings.json):")
    # Ubah backslash jadi forward slash untuk JSON
    print(str(potential_path).replace("\\", "/"))
else:
    print("qmlls tidak ditemukan otomatis. Coba cari manual di folder .venv")
print("-" * 30)
