import os
import subprocess
from pathlib import Path
from typing import override, Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface): # pyright: ignore[reportMissingTypeArgument]
    @override
    def initialize(self, version: str, build_data: dict[str, Any]): # pyright: ignore[reportExplicitAny]
        """
        Metode ini dijalankan sebelum proses build dimulai.
        """
        print("Mencari dan mengompilasi file .qrc...")

        # Tentukan path ke direktori sumber
        source_dir = Path("src/myapp")

        # Cari semua file .qrc di dalam direktori sumber
        for qrc_file in source_dir.glob("*.qrc"):
            output_file = qrc_file.with_name(f"{qrc_file.stem}_rc.py")
            print(f"  -> Mengompilasi {qrc_file} ke {output_file}")

            try:
                _ = subprocess.run(
                    ["pyside6-rcc", str(qrc_file), "-o", str(output_file)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"ERROR: Gagal mengompilasi {qrc_file}")
                print(e.stderr) # pyright: ignore[reportAny]
                raise

            # Paksa Hatch untuk menyertakan file .py yang baru dibuat
            # dalam paket distribusi (wheel)
            # Path dihitung relatif terhadap root proyek
            include_path = os.path.join(str(source_dir), output_file.name)
            if include_path not in build_data["force_include"]:
                #build_data["force_include"][str(output_file)] = include_path
                target_path_in_wheel = os.path.join("myapp", output_file.name)
                target_path_in_wheel = os.path.join("myapp", output_file.name)

                #print(f"  -> Menyertakan {output_file.name} dalam build")
                print(f"  -> Menyertakan {output_file.name} sebagai {target_path_in_wheel} dalam build")
