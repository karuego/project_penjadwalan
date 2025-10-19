from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
import subprocess

class build_py(_build_py):
    def run(self):
        subprocess.run(["pyside6-rcc", "application.qrc", "-o", "application_rc.py"], check=True)
        super().run()

setup(
    name="myapp",
    version="0.1.0",
    py_modules=["main"],  # ← hanya file .py langsung, bukan package
    cmdclass={"build_py": build_py},
)

