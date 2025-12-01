import os
import PySide6

# Ambil lokasi folder instalasi PySide6
pyside_dir = os.path.dirname(PySide6.__file__)
qml_dir = os.path.join(pyside_dir, "qml")

print("-" * 30)
print("MASUKKAN PATH INI KE VS CODE:")
print(qml_dir.replace("\\", "/")) # Ubah backslash jadi forward slash agar JSON valid
print("-" * 30)
